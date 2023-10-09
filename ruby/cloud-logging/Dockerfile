FROM ruby:3.2.2-slim

ENV APP_ENV production

RUN bundle config --global set frozen 'true'

WORKDIR /usr/src/app

COPY Gemfile Gemfile.lock ./
RUN bundle install

COPY main.rb ./

CMD ["ruby", "main.rb"]