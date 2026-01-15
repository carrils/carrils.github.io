---
layout: archive
title: "MITRE Projects"
permalink: /projects/
author_profile: false
---
<style>
  .archive {
    width: 80%;
    margin: 0 auto;
    float: none;
    padding-right: 0;
  }
  
  @media (min-width: 80em) {
    .archive {
      width: 70%;
    }
  }
</style>
All projects at MITRE follow a standard model of not being standard.<br />
This in practice means that each project is unique and has its own set of differences according to how the Project Leader captains the ship. 
They do however follow a general structure of having a Project Leader delivering contractually defined work, executed by Task Leaders and often assisted by a Deputy Project Lead.

The actual project work is outlined in a Statement of Work (SOW) document that details scope, objectives, deliverables and a timeline.
These objectives and deliverables are broken down and categorized into tasks.
These tasks are then managed and ensured by Task Leaders that are usually recognized SMEs in their respective task. 
Task leaders are assisted by individual contributors to the project, typically in the form of engineers and other personnel.
<br />
<br />
Below I have compiled a list of some of the projects I have had the chance to work on, and have mentioned on my CV.

Project Experience
======
<ul>
    {% for post in site.projects %}
        <li>{% include archive-single.html %}
    {% endfor %}

