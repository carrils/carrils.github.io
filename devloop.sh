#!/bin/zsh
echo "$(./scripts/update_cv_json.sh)"
bundle exec jekyll clean
bundle exec jekyll serve -l -H localhost
