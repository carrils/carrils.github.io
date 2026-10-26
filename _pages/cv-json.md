---
# this file is called cv-json because it is derived from many json files after running the python script
layout: archive
#title: "Curriculum vitae"
permalink: cv/
author_profile: true
redirect_from:
  - /resume-json
  - /about-me/
---

{% include base_path %}

{% include cv-template.html %}

<div class="cv-download-links">
  <a href="../files/Long-CV.pdf" class="btn btn--primary" download="CV_Sam_Carrillo_{{ 'now' | date: '%m-%d' }}.pdf">Download CV as PDF</a>
</div>