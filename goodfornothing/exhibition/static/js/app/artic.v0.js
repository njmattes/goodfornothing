(function() {
  'use strict';

  //https://metmuseum.github.io/

  const URL = 'https://api.artic.edu/api/v1/search';
  let object_ids = [];
  let objects = [];
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
    const TOTAL_WORKS = encodeURI('?query[exists]=image_id&limit=0');
    let query = {
      resources: 'artworks',
      fields: ['id', 'title', 'artist_title', 'image_id', 'date_display',
        'thumbnail', ],
      boost: false, limit: 50,
      query: { function_score: {
        query: { bool: { filter: [
          { term: { is_public_domain: true, }, },
          { exists: { field: 'image_id', }, },
        ], }, },
        boost_mode: 'replace',
        random_score: { field: 'id', seed: 1, },
      }, }
    };
    if (object_n === 0) {
      return fetch(
        URL, {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify(query)
        })
        .then(response => response.json())
        .then(data => {
          objects = data;
        });
    } else {
      return new Promise((resolve) => resolve());
    }
  };

  // const get_random_image = function get_random_image() {
  //   return get_object_ids()
  //     .then(() => {
  //       idx = object_ids[Math.floor(Math.random() * object_n)];
  //       const OBJECT_ID = encodeURI(`objects/${idx}`);
  //       return fetch(URL+OBJECT_ID); })
  //     .then(response => response.json())
  //     .then(function(data) {
  //       is_public = data.isPublicDomain;
  //       img_url = data.primaryImage;
  //       console.log(data.isPublicDomain);
  //       if (!(data.isPublicDomain)) {
  //         console.log('bar?');
  //         object_ids.splice(object_ids.indexOf(idx), 1);
  //         --object_n;
  //       }
  //     })
  //     .then(() => [idx, is_public, img_url])
  // };

  get_object_ids().then(() => console.log(objects));

  // const get_public_image = function get_public_image() {
  //   get_random_image().then(data => {
  //     if (data[1]) {
  //       img.setAttribute('src', img_url);
  //       is_public = false
  //     } else {
  //       get_public_image();
  //     }
  //   })
  // };

  // button.addEventListener('click', get_public_image);

})();