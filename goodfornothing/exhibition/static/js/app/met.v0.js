(function() {
  'use strict';

  //https://metmuseum.github.io/

  const URL = 'https://collectionapi.metmuseum.org/public/collection/v1/';
  let object_ids = [];
  let object_n = 0;
  let is_public = false;
  let img_url = false;
  let idx;

  let img = document.createElement('img');
  let main = document.getElementsByTagName('main')[0];
  let button = document.createElement('a');
  img.setAttribute('class', 'exhibition-image');
  button.setAttribute('href', '#');
  button.textContent = 'press';
  main.appendChild(img);
  main.appendChild(button);

  const get_object_ids = function get_object_ids() {
    const TOTAL_WORKS = encodeURI('objects');
    if (object_n === 0) {
      return fetch(URL+TOTAL_WORKS)
        .then(response => response.json())
        .then(data => {
          object_ids = data.objectIDs;
          object_n = data.total;
        });
    } else {
      return new Promise((resolve) => resolve());
    }
  };

  const get_random_image = function get_random_image() {
    return get_object_ids()
      .then(() => {
        idx = object_ids[Math.floor(Math.random() * object_n)];
        const OBJECT_ID = encodeURI(`objects/${idx}`);
        return fetch(URL+OBJECT_ID); })
      .then(response => response.json())
      .then(function(data) {
        is_public = data.isPublicDomain;
        img_url = data.primaryImage;
        console.log(data.isPublicDomain);
        if (!(data.isPublicDomain)) {
          console.log('bar?');
          object_ids.splice(object_ids.indexOf(idx), 1);
          --object_n;
        }
      })
      .then(() => [idx, is_public, img_url])
  };

  get_object_ids().then(() => console.log(object_n));

  const get_public_image = function get_public_image() {
    get_random_image().then(data => {
      if (data[1]) {
        img.setAttribute('src', img_url);
        is_public = false
      } else {
        get_public_image();
      }
    })

  };

  button.addEventListener('click', get_public_image);

})();