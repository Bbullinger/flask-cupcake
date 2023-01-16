const BASE_URL = "http://localhost:5000/api";

// This will give us the HTML used to display each cupcake
const cupcakeList = document.querySelector("#cupcakeList");

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
  cupcakePSize.innerText = `${cupcake.rating}/10`;
  cupcakeLi.append(cupcakePRating);

  const cupcakeImage = document.createElement("img");
  cupcakeImage.src = cupcake.image_url;
  cupcakeImage.setAttribute("class", "cupcakeImage");
  cupcakeDiv.append(cupcakeImage);

  console.log(
    cupcakeDiv,
    cupcakeLi,
    cupcakePFlavor,
    cupcakePSize,
    cupcakePRating
  );
}

//   return `<div class="cupcake" data-cupcake-id="cupcake.id">
//     <li>
//         <p>${cupcake.flavor}</p>
//         <p>${cupcake.size}</p>
//         <p>${cupcake.rating}</p>
//     </li>
//     <img class="cupcakeImage" src="cupcake.image_url">
// </div>`;

async function showAllCupcakes() {
  const response = await axios.get(`${BASE_URL}/cupcakes`);

  for (let cupcake of response.data.cupcakes) {
    cupcakeHTML(cupcake);
  }
}

showAllCupcakes();
