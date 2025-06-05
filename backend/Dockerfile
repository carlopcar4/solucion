FROM ruby:3.2.2

RUN apt-get update -qq && apt-get install -y nodejs postgresql-client && apt install nano

WORKDIR /app

COPY Gemfile Gemfile.lock ./

RUN bundle install

COPY . .

COPY entrypoint.sh /usr/bin/
RUN chmod +x /usr/bin/entrypoint.sh

ENTRYPOINT [ "entrypoint.sh" ]

CMD ["rails", "server", "-b", "0.0.0.0", "-p", "4000"]