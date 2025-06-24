# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the bin/rails db:seed command (or created alongside the database with db:setup).
#
# Examples:
#
#   movies = Movie.create([{ name: "Star Wars" }, { name: "Lord of the Rings" }])
#   Character.create(name: "Luke", movie: movies.first)
# You can remove the 'faker' gem if you do not want Decidim seeds.
name = "hola"
port = 3002
start_date = Date.today
end_date = start_date + 30
id = 2

puts "Creando organización: #{name}"

o = Decidim::Organization.create(
  # id: id, # El ID generalmente se autoincrementa, Decidim podría no necesitarlo en 'create'
  host: "#{name}.localhost",
  name: { es: "#{name}" },
  description: {es: "Descripción para #{name}" },
  available_locales: [:es],
  default_locale: :es, # Como símbolo
  reference_prefix: "hola" # <-- ¡ESTO ES CRUCIAL! Debe ser único
)