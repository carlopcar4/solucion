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

COPY Gemfile Gemfile.lock package.json yarn.lock /app/
RUN bundle install
RUN yarn install

COPY . /app

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]