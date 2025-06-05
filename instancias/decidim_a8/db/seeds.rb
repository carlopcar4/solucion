# backend/db/seeds.rb
require "open-uri"
require "date"

# --- 0) Si quieres evitar correrlo en entornos distintos a la instancia, 
#     podrías hacer un guard: abort o return unless ENV["DB_NAME"].present?

name           = ENV.fetch("NAME", nil)
slug_org       = ENV.fetch("DB_NAME", nil)
org_id         = ENV["ID"]&.to_i
collaborations = ENV.fetch("COLLABORATIONS", "").split(",").map(&:strip).reject(&:empty?)
services       = ENV.fetch("SERVICES", "").split(",").map(&:strip).reject(&:empty?)
logo_url       = ENV.fetch("LOGO", "")
banner_url     = ENV.fetch("BANNER", "")

if name.nil? || slug_org.nil?
  puts "⚠️  No hay variables NAME/DB_NAME en el entorno. Saltando seeds."
  exit 0
end

puts "⚙️  Sembrando instancia: #{name} (slug: #{slug_org})"

# 1) Organización
org = Decidim::Organization.find_or_initialize_by(slug: slug_org)
org.id                        = org_id if org_id
org.host                      = "#{slug_org}.localhost"
org.name                      = { es: name }
org.description               = { es: "Instancia automática para #{name}" }
org.reference_prefix          = name[0..2].upcase
org.available_locales         = [:es]
org.default_locale            = "es"
org.highlighted_content_banner_enabled           = true
org.highlighted_content_banner_title             = { es: "Bienvenido a #{name}" }
org.highlighted_content_banner_short_description = { es: "Descubre procesos en #{name}" }
org.highlighted_content_banner_action_title      = { es: "Ver procesos" }
org.highlighted_content_banner_action_subtitle   = { es: "Participa ahora" }
org.highlighted_content_banner_action_url        = "/es-#{slug_org}/procesos"
org.save!

# 2) Adjuntar logo
if logo_url.present?
  begin
    org.logo.purge if org.logo.attached?
    org.logo.attach(
      io:           URI.open(logo_url),
      filename:     "logo-#{slug_org}#{File.extname(logo_url)}",
      content_type: Rack::Mime.mime_type(File.extname(logo_url))
    )
    puts "   • Logo cargado desde #{logo_url}"
  rescue => e
    puts "   ❗ Error al adjuntar logo: #{e.message}"
  end
end

# 3) Adjuntar banner
if banner_url.present?
  begin
    org.highlighted_content_banner_image.purge if org.highlighted_content_banner_image.attached?
    org.highlighted_content_banner_image.attach(
      io:           URI.open(banner_url),
      filename:     "banner-#{slug_org}#{File.extname(banner_url)}",
      content_type: Rack::Mime.mime_type(File.extname(banner_url))
    )
    puts "   • Banner cargado desde #{banner_url}"
  rescue => e
    puts "   ❗ Error al adjuntar banner: #{e.message}"
  end
end

# 4) Crear un proceso participativo si hay módulos marcados
if collaborations.any? || services.any?
  proc_title = "Proceso de #{name}"
  start_date = Date.today
  end_date   = start_date + 30

  process = Decidim::ParticipatoryProcess.find_or_create_by!(slug: proc_title.parameterize) do |p|
    p.organization      = org
    p.title             = { es: proc_title }
    p.subtitle          = { es: "Participa en los módulos de #{name}" }
    p.description       = { es: "Este proceso agrupa los componentes marcados en .env" }
    p.short_description = { es: "Participa en #{name}" }
    p.published_at      = DateTime.now
    p.start_date        = start_date
    p.end_date          = end_date
  end
  puts "   • Proceso participativo creado: #{proc_title}"

  admin_email = "admin@#{slug_org}.local"
  admin = Decidim::User.find_or_create_by!(email: admin_email) do |u|
    u.name                  = "Admin #{slug_org}"
    u.nickname              = "admin_#{slug_org}"
    u.password              = "Contraseña123!"
    u.password_confirmation = "Contraseña123!"
    u.organization          = org
    u.confirmed_at          = Time.now
    u.tos_agreement         = true
  end

  (collaborations + services).each_with_index do |comp_name, idx|
    manifest = case comp_name.downcase
    when "proposals" then "proposals"
    when "surveys"   then "surveys"
    when "meetings"  then "meetings"
    else "proposals"
    end

    c = Decidim::Component.find_or_initialize_by(
      participatory_space: process,
      manifest_name:       manifest
    )
    c.name     = { es: comp_name }
    c.weight   = idx + 1
    c.settings = { "comments_enabled" => true } if c.new_record?
    c.save!
    puts "     ↳ Componente creado: #{comp_name} (manifest: #{manifest})"
  end

  # 5) Una propuesta de prueba
  first_component = Decidim::Component.where(participatory_space: process).first
  if first_component
    Decidim::Proposals::ProposalBuilder.create(
      attributes: {
        title:     { es: "Propuesta de ejemplo para #{name}" },
        body:      { es: "Texto de prueba generado automáticamente." },
        component: first_component
      },
      author:      admin,
      action_user: admin
    )
    puts "     ↳ Propuesta de ejemplo creada"
  end
end

puts "✅ Seeds completados para #{name}"
