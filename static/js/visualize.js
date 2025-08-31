let asteroids = [];
let currentIndex = 0;

async function loadAsteroids() {
  const res = await fetch("/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({})
  });

  const data = await res.json();
  asteroids = data.asteroids.slice(0, 10);

  showAsteroid(0);
}

function showAsteroid(index) {
  if (!asteroids.length) return;

  const asteroidEl = document.querySelector(".asteroid");
  const glowEl = document.querySelector(".glow");
  const nameEl = document.getElementById("asteroid-name");
  const infoEl = document.getElementById("asteroid-info");
  const section = document.querySelector(".asteroid-section");

  // fade out
  section.style.opacity = 0;

  setTimeout(() => {
    const a = asteroids[index];

    // random asteroid image
    const randomIndex = Math.floor(Math.random() * 7) + 1;
    asteroidEl.style.backgroundImage = `url("/static/assets/asteroid${randomIndex}.png")`;

    // glow color
    glowEl.style.background = a.is_potential_hazard
      ? "radial-gradient(circle, rgba(0,255,0,0.6), rgba(0,0,0,0))"
      : "radial-gradient(circle, rgba(0,200,255,0.6), rgba(0,0,0,0))";

    // name
    nameEl.textContent = a.name;

    // hazard info
    let hazardVal = (a.is_potential_hazard === 1 || a.is_potential_hazard === true) ? "Yes" : "No";
    infoEl.innerHTML = `
      Hazardous: <strong>${hazardVal}</strong><br>
      Torino Rating: <strong>${a.torino_rating ?? a.danger_rating ?? "N/A"}</strong>
    `;

    // fill dashboard
    const dashLeft = document.querySelector(".dash-left");
    const dashRight = document.querySelector(".dash-right");
    dashLeft.innerHTML = `
      <p>Absolute Magnitude: ${a.absolute_magnitude_h}</p>
      <p>Jupiter Tisserand: ${a.jupiter_tisserand_invariant}</p>
      <p>Eccentricity: ${a.eccentricity}</p>
      <p>Inclination: ${a.inclination}</p>
      <p>Asc. Node Long.: ${a.ascending_node_longitude}</p>
      <p>Perihelion Distance: ${a.perihelion_distance}</p>
    `;
    dashRight.innerHTML = `
      <p>Perihelion Argument: ${a.perihelion_argument}</p>
      <p>Mean Anomaly: ${a.mean_anomaly}</p>
      <p>Diameter (max): ${a.estimated_diameter_max}</p>
      <p>Rel. Velocity (km/s): ${a.relative_velocity_kmps}</p>
      <p>Miss Dist (AU): ${a.miss_distance_in_astronomical}</p>
      <p>Torino Rating: ${a.torino_rating ?? a.danger_rating ?? "N/A"}</p>
    `;

    // fade in
    section.style.opacity = 1;
  }, 300);
}

// arrows
document.getElementById("prev").addEventListener("click", () => {
  currentIndex = (currentIndex - 1 + asteroids.length) % asteroids.length;
  showAsteroid(currentIndex);
});
document.getElementById("next").addEventListener("click", () => {
  currentIndex = (currentIndex + 1) % asteroids.length;
  showAsteroid(currentIndex);
});

// scroll navigation
window.addEventListener("wheel", (e) => {
  if (e.deltaY > 0) {
    currentIndex = (currentIndex + 1) % asteroids.length;
  } else {
    currentIndex = (currentIndex - 1 + asteroids.length) % asteroids.length;
  }
  showAsteroid(currentIndex);
});

// dashboard toggle
document.getElementById("menu-btn").addEventListener("click", () => {
  document.getElementById("dashboard").classList.toggle("active");
});

loadAsteroids();
