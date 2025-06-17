FROM ruby:3.2.2

ENV DEBIAN_FRONTEND noninteractive
ENV NODE_MAJOR=20

# Install system dependencies
RUN apt-get update -qq && apt-get install -y \
    build-essential \
    graphviz \
    imagemagick \
    libicu-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install node
RUN mkdir -p /etc/apt/keyrings
RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
RUN echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list
RUN apt-get update -qq && apt-get install -y \
    nodejs \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g yarn

# Create workdir - no need to copy code yet, as it will be mounted
WORKDIR /app

# Installs bundler dependencies (this assumes Gemfile/Gemfile.lock are available during build, which they would be if you copy them first)
# Consider copying Gemfile/Gemfile.lock before this if they are not in the build context root.
# If using volumes, the bundle install during build might be less critical if you handle it in the entrypoint of the container.
# For development, you might want to run `bundle install` as part of your `command` in `docker-compose.yml` if the `Gemfile` changes often.
# For now, let's assume Gemfile is at the root of the build context when building this image.
COPY Gemfile Gemfile.lock /app/
RUN gem install bundler:2.4.22
RUN bundle install

# No need for ADD . /app here if you are mounting the code as a volume for development.
# ADD . /app

# Compile assets (npm i, npm i -g yarn) - These should also be in a proper workdir
# If /app is mounted, these operations will affect your host's node_modules, which is usually desired.
# Ensure package.json and yarn.lock are in the mounted /app directory.
# You might want to run `npm install` or `yarn install` as part of your `command` in docker-compose.yml
# RUN npm i
# RUN npm i -g yarn