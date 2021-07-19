(function() {
  'use strict';

  //https://openaccess-api.clevelandart.org/

  const URL = 'https://openaccess-api.clevelandart.org/api/artworks/';
  const TYPES = 'Painting+Drawing+Photograph';
  // const TYPES = 'Painting';
  let object_n = 0;
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

    const TOTAL_WORKS = encodeURI(
      `?type=${TYPES}&has_image=1&limit=1`);
    if (object_n === 0) {
      return fetch(URL+TOTAL_WORKS)
        .then(response => response.json())
        .then(data => {
          console.log(data)
          object_n = data.info.total;
        });
    } else {
      return new Promise((resolve) => resolve());
    }
  };

  const get_random_image = function get_random_image() {
    return get_object_ids()
      .then(() => {
        idx = Math.floor(Math.random() * object_n);
        console.log(idx);
        const OBJECT_ID = encodeURI(
          `?type=${TYPES}&has_image=1&limit=1&skip=${idx}`);
        return fetch(URL+OBJECT_ID); })
      .then(response => response.json())
      .then(function(data) {
        img_url = data.data[0].images.web.url;
      })
      .then(() => [idx, img_url])
  };

  get_object_ids().then(() => console.log(object_n));

  const get_image = function get_image() {
    get_random_image().then(data => {
      img.setAttribute('src', data[1]);
    });
  };

  button.addEventListener('click', get_image);

})();