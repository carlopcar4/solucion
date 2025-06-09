class CouncilsController < ApplicationController
  require 'json'
  require 'net/http'
  require 'uri'

  include Rails.application.routes.url_helpers
  skip_before_action :verify_authenticity_token


  def index
	@councils = Council.all
	render json: @councils
  end

  def show
	@council = Council.find(params[:id])
	if @council.logo.attached? and @council.banner.attached?
		logo_url = url_for(@council.logo)
		banner_url = url_for(@council.banner)
		res = @council.as_json.merge(logo_url: logo_url, banner_url: banner_url)
		render json: res, status: :accepted
	else
		render json: @council
	end
  end


  def create
    @council = Council.new(council_params)
    @council.logo.attach(params[:logo])
    @council.banner.attach(params[:banner])
    if @council.save
	begin
		logo_url = url_for(@council.logo)
		banner_url = url_for(@council.banner)
		uri = URI('http://flask:4001/crear_instancia')
		req = Net::HTTP::Post.new(uri, 'Content-Type' => 'application/json')
		req.body = { id: @council.id, name: @council.name, puerto_org: @council.puerto_org, 
			logo: logo_url, banner: banner_url, collaborations: @council.collaborations,
			services: @council.services }.to_json
		Net::HTTP.start(uri.hostname, uri.port) do |http|
			http.request(req)
		end
	rescue => e
		Rails.logger.error("Error creando instancia : #{e.message}")
	end

      sol = @council.as_json.merge(logo_url: logo_url, banner_url: banner_url)

      render json: sol, status: :created
    else
      render json: @council.errors, status: :unprocessable_entity
    end
  end


  def update
	begin
		@council = Council.find(params[:id])
		if @council.update(params.permit(collaborations: [], services: []))
			render json: @council, status: :ok
		else
			render json: @council, status: :no_content
		end
	rescue Exception => e
		Rails.logger.error(e)
		render json: @council.errors, status: :bad_request
	end
  end


  def destroy
	@council = Council.find(params[:id])
	if @council.destroy
		render json: {message: "Municipio eliminado correctamente"}
	else
		render json: @council.errors, status: :not_found
	end
  end



  private

  def council_params
    params.permit(:name, :province, :population, :puerto_org, :logo, :banner, :multi_tenant, collaborations: [], services: [])
  end

end
