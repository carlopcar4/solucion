FROM decidim/decidim:0.29.3

WORKDIR /app

COPY Gemfile Gemfile.lock ./

RUN bundle install --jobs $(nproc) --without development test

COPY . ./

EXPOSE 3000

CMD ["bundle", "exec", "puma", "-C", "config/puma.rb"]