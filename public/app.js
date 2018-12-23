"use strict";

const URLS = [
  "https://www.hackster.io/projects",
  "https://hackdash.org/projects",
  "https://devpost.com/software"
];

const search_projects = function(key) {
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
