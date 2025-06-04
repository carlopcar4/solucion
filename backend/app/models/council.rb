class Council < ApplicationRecord
 has_one_attached :logo
 has_one_attached :banner
 validates :name, :province, :population, :puerto_org, presence: true 
end
