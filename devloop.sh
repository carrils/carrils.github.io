#!/bin/zsh
bundle exec jekyll clean
bundle exec jekyll build
bundle exec jekyll serve -l -H localhost
