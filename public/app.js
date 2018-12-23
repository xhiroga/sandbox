"use strict";

const URLS = [
  "https://hackaday.io/project",
  "https://www.hackster.io/projects",
  "https://www.hackreactor.com/student-projects/",
  "http://www.hackathon.io/projects",
  "https://hackdash.org/projects",
  "https://devpost.com/software",
  "https://www.ideasvoice.com/en/pub/project/",
  "https://www.programmableweb.com/mashup/",
  "https://hackerspace.govhack.org/projects",
  "https://makezine.com/projects/",
  "spaceappschallenge.org/project",
  "https://protopedia.net/prototype",
  "https://opendata.cityofnewyork.us/projects"
];

const search_projects = function() {
  const head = "https://www.google.com/search";

  const keywords = $("#keywords")
    .val()
    .split(" ")
    .reduce((word, words) => words + "+" + word);

  const sites = URLS.map(url => "site:" + url)
    .map(url => encodeURIComponent(url))
    .reduce((site, current_sites) => current_sites + "+OR+" + site);

  const url = head + "?q=" + keywords + "+" + sites;
  console.log(url);
  window.open(url);
};
