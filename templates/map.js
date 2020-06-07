const makeAttribution = () => {
  return (
    'Geodaten &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a>-Mitwirkende, ' +
    'Abfuhrtermine <a href="https://opendata.stadt-muenster.de/dataset/entsorgungskalender-2020-der-abfallwirtschaftsbetriebe-m%C3%BCnster-awm">Stadt Münster</a>'
  );
};

const map = L.map("map").setView([51.96, 7.62], 12);

L.tileLayer("https://{s}.tile.openstreetmap.de/{z}/{x}/{y}.png", {
  maxZoom: 18,
  attribution: makeAttribution(),
}).addTo(map);

const streetsLayer = L.geoJSON({ features: [], type: 'FeatureCollection' }).addTo(map);

const fetchData = async (date) => {
  const resp = await fetch(`/data/${date}.json`);
  return resp.json();
}

let state = {
  selectedDate: null,
  selectedWaste: null,
  data: Object.create(null),
}

const updateState = async (newState) => {
  state = { ...state, ...newState };

  const { selectedDate, selectedWaste } = state;

  let data = state.data[selectedDate];

  if (!data) {
    data = await fetchData(selectedDate);
    state.data[selectedDate] = data;
  }


  for (const link of document.querySelectorAll("a[role=button]")) {
    const { date, wastetype } = link.dataset;
    if (date === selectedDate || wastetype === selectedWaste) {
      link.classList.add('selected');
    } else {
      link.classList.remove('selected');
    }
  }

  streetsLayer.clearLayers();
  for (const [, { g, w }] of Object.entries(data)) {
    if (w.includes(selectedWaste) && g !== null) {
      streetsLayer.addData(g);
    }
  }
  map.fitBounds(streetsLayer.getBounds());
}

const init = () => {
  let selectedDate = null;
  let selectedWaste = null;

  for (const wasteLink of document.querySelectorAll("a[data-wastetype]")) {
    const { wastetype } = wasteLink.dataset;

    if (selectedWaste === null) {
      selectedWaste = wastetype;
    }

    wasteLink.addEventListener('click', () => updateState({ selectedWaste: wastetype }));
  }

  for (const dateLink of document.querySelectorAll("li:not([hidden=true]) a[role=button]")) {
    const { date } = dateLink.dataset;

    if (selectedDate === null) {
      selectedDate = date;
    }

    dateLink.addEventListener('click', () => updateState({ selectedDate: date }));
  }

  updateState({ selectedWaste, selectedDate });
}

init();
