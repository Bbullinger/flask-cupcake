const BASE_URL = "http://localhost:5000/api";

// This will give us the HTML used to display each cupcake
const cupcakeList = document.querySelector("#cupcakeList");

//DOM elements related to form to add a new cupcake
const cupcakeForm = document.querySelector("#cupcakeForm");
const addFlavor = document.querySelector("cupcakeFlavor");
const addRating = document.querySelector("cupcakeRating");
const addSize = document.querySelector("cupcakeSize");
const addImageURL = document.querySelector("cupcakeImageURL");

function cupcakeHTML(cupcake) {
  const cupcakeDiv = document.createElement("div");
  cupcakeDiv.setAttribute("class", "cupcake");
  cupcakeDiv.setAttribute("data-cupcake-id", cupcake.id);
  cupcakeList.append(cupcakeDiv);

  const cupcakeLi = document.createElement("li");
  cupcakeDiv.append(cupcakeLi);

  const cupcakePFlavor = document.createElement("p");
  cupcakePFlavor.innerText = cupcake.flavor;
  cupcakeLi.append(cupcakePFlavor);

  const cupcakePSize = document.createElement("p");
  cupcakePSize.innerText = cupcake.size;
  cupcakeLi.append(cupcakePSize);

  const cupcakePRating = document.createElement("p");
  cupcakePRating.innerText = `${cupcake.rating}/10`;
  cupcakeLi.append(cupcakePRating);

  const cupcakeImage = document.createElement("img");
  cupcakeImage.src = cupcake.image_url;
  cupcakeImage.setAttribute("class", "cupcakeImage");
  cupcakeDiv.append(cupcakeImage);

  console.log(cupcake.size);

  //HTML should look like:
  // `<div class="cupcake" data-cupcake-id="cupcake.id">
  //     <li>
  //         <p>${cupcake.flavor}</p>
  //         <p>${cupcake.size}</p>
  //         <p>${cupcake.rating}</p>
  //     </li>
  //     <img class="cupcakeImage" src="cupcake.image_url">
  // </div>`;
}

async function showAllCupcakes() {
  const response = await axios.get(`${BASE_URL}/cupcakes`);

  for (let cupcake of response.data.cupcakes) {
    cupcakeHTML(cupcake);
  }
}

showAllCupcakes();

async function submitCupcakeForm(e) {
  e.preventDefault();

  //grab all values from cupcake form
  const flavor = addFlavor.val();
  const rating = addRating.val();
  const size = addSize.val();
  const imageURL = addImageURL.val();

  const postCupcakeResp = await axios.post(`${BASE_URL}/cupcakes`, {
    flavor,
    rating,
    size,
    imageURL,
  });
  const newCupcake = cupcakeHTML(postCupcakeResp.data.cupcake);
  console.log(newCupcake);
}

cupcakeForm.addEventListener("submit", submitCupCakeForm(e));
