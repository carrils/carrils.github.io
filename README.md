## Locations of key files/directories
* Basic config options: _config.yml
* Top navigation bar config: _data/navigation.yml
* Single pages: _pages/
* Footer: _includes/footer.html
* Static files (like PDFs): /files/
* Profile image (can set in _config.yml): images/profile.png
* Collections of pages are .md or .html files in:
	* _publications/
	* _portfolio/
	* _posts/
	* _teaching/
	* _talks/

## Theme front page:
	`_pages/about.md`

## steps to update /cv-json/
* update _pages/cv.md
* run /scripts/update_cv_json.sh

jekyll liquid variables: https://jekyllrb.com/docs/variables/
site.data == A list containing the data loaded from the YAML files located in the _data directory.

on running `jekyll new .`
these files are made:
* _config.yml
* _posts
* 404.html
* about.markdown
* Gemfile
* Gemfile.lock
* index.markdown
