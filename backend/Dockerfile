FROM ruby:3.2.2

# 1) Instalar dependencias de sistema de una sola vez
RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends \
    nodejs \
    postgresql-client \
    nano && \
    rm -rf /var/lib/apt/lists/*

# 2) Establecer el directorio de trabajo
WORKDIR /app

# 3) Copiar Gemfile y Gemfile.lock y luego instalar gemas
COPY Gemfile Gemfile.lock ./
RUN bundle install --jobs 4 --retry 3

# 4) Copiar el resto del código en /app
COPY . .

# 5) Copiar entrypoint.sh y darle permisos de ejecución
COPY entrypoint.sh /usr/bin/entrypoint.sh
RUN chmod +x /usr/bin/entrypoint.sh

# 6) Definir entrypoint
ENTRYPOINT [ "/usr/bin/entrypoint.sh" ]

# 7) Puerto por defecto para Rails
CMD ["rails", "server", "-b", "0.0.0.0", "-p", "4000"]
