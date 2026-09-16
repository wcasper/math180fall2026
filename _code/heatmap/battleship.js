(() => {
  "use strict";

  const SIZE = 10;
  const CELL_COUNT = SIZE * SIZE;
  const STATES = ["unknown", "miss", "hit", "sunk"];
  const LETTERS = "ABCDEFGHIJ";

  const boardElement = document.getElementById("board");
  const columnLabels = document.getElementById("column-labels");
  const rowLabels = document.getElementById("row-labels");
  const toolButtons = [...document.querySelectorAll("[data-tool]")];
  const fleetInputs = [...document.querySelectorAll("#fleet-list input")];
  const sampleCount = document.getElementById("sample-count");
  const runButton = document.getElementById("run-simulation");
  const clearButton = document.getElementById("clear-board");
  const exampleButton = document.getElementById("load-example");
  const statusElement = document.getElementById("status");
  const summaryElement = document.getElementById("summary");
  const topTargetsElement = document.getElementById("top-targets");

  let selectedTool = "unknown";
  let isPainting = false;
  let simulationToken = 0;
  const boardState = Array(CELL_COUNT).fill("unknown");
  const cells = [];

  function indexToCoordinate(index) {
    return `${LETTERS[index % SIZE]}${Math.floor(index / SIZE) + 1}`;
  }

  function setStatus(message, type = "idle") {
    statusElement.textContent = message;
    statusElement.className = `status ${type}`;
  }

  function clearProbabilities() {
    cells.forEach((cell) => {
      cell.classList.remove("has-probability");
      cell.style.removeProperty("--p");
      cell.style.removeProperty("--heat-hue");
      cell.style.removeProperty("--heat-saturation");
      cell.style.removeProperty("--heat-lightness");
      cell.style.removeProperty("--heat-color");
      cell.style.removeProperty("--heat-ink");
      if (boardState[Number(cell.dataset.index)] === "unknown") cell.textContent = "";
    });
    topTargetsElement.replaceChildren();
  }

  function renderCell(index) {
    const cell = cells[index];
    const state = boardState[index];
    cell.className = `cell state-${state}`;
    cell.textContent = "";
    cell.setAttribute("aria-label", `${indexToCoordinate(index)}: ${state === "hit" ? "unresolved hit" : state}`);
    cell.setAttribute("aria-selected", state !== "unknown" ? "true" : "false");
  }

  function paintCell(index) {
    if (boardState[index] === selectedTool) return;
    boardState[index] = selectedTool;
    clearProbabilities();
    renderCell(index);
    summaryElement.textContent = "The evidence changed. Run the simulation to update the probabilities.";
  }

  function initializeBoard() {
    [...LETTERS].forEach((letter) => {
      const label = document.createElement("span");
      label.textContent = letter;
      columnLabels.append(label);
    });
    for (let row = 1; row <= SIZE; row += 1) {
      const label = document.createElement("span");
      label.textContent = row;
      rowLabels.append(label);
    }
    for (let index = 0; index < CELL_COUNT; index += 1) {
      const cell = document.createElement("button");
      cell.type = "button";
      cell.dataset.index = index;
      cell.setAttribute("role", "gridcell");
      cell.addEventListener("pointerdown", (event) => {
        event.preventDefault();
        isPainting = true;
        paintCell(index);
      });
      cell.addEventListener("pointerenter", () => {
        if (isPainting) paintCell(index);
      });
      cell.addEventListener("keydown", (event) => {
        const row = Math.floor(index / SIZE);
        const col = index % SIZE;
        const moves = { ArrowUp: [-1, 0], ArrowDown: [1, 0], ArrowLeft: [0, -1], ArrowRight: [0, 1] };
        if (moves[event.key]) {
          event.preventDefault();
          const [dr, dc] = moves[event.key];
          const nextRow = Math.max(0, Math.min(SIZE - 1, row + dr));
          const nextCol = Math.max(0, Math.min(SIZE - 1, col + dc));
          cells[nextRow * SIZE + nextCol].focus();
        } else if (event.key === " " || event.key === "Enter") {
          event.preventDefault();
          paintCell(index);
        }
      });
      boardElement.append(cell);
      cells.push(cell);
      renderCell(index);
    }
  }

  function getShips() {
    return fleetInputs
      .filter((input) => input.checked)
      .map((input, index) => ({ length: Number(input.value), name: input.dataset.name, id: `${input.dataset.name}-${index}` }))
      .sort((a, b) => b.length - a.length);
  }

  function makePlacement(startRow, startCol, length, horizontal) {
    const squares = [];
    for (let offset = 0; offset < length; offset += 1) {
      const row = startRow + (horizontal ? 0 : offset);
      const col = startCol + (horizontal ? offset : 0);
      squares.push(row * SIZE + col);
    }
    return { squares };
  }

  function candidatePlacements(length, forbidden) {
    const candidates = [];
    for (let row = 0; row < SIZE; row += 1) {
      for (let col = 0; col < SIZE; col += 1) {
        if (col + length <= SIZE) {
          const placement = makePlacement(row, col, length, true);
          if (placement.squares.every((square) => !forbidden.has(square))) candidates.push(placement);
        }
        if (row + length <= SIZE) {
          const placement = makePlacement(row, col, length, false);
          if (placement.squares.every((square) => !forbidden.has(square))) candidates.push(placement);
        }
      }
    }
    return candidates;
  }

  function shuffled(items) {
    const copy = items.slice();
    for (let i = copy.length - 1; i > 0; i -= 1) {
      const j = Math.floor(Math.random() * (i + 1));
      [copy[i], copy[j]] = [copy[j], copy[i]];
    }
    return copy;
  }

  function coversAllHits(fleet, hits) {
    if (hits.size === 0) return true;
    const occupied = new Set(fleet.flatMap((placement) => placement.squares));
    return [...hits].every((hit) => occupied.has(hit));
  }

  function findInitialFleet(ships, candidatesByShip, hits) {
    const fleet = Array(ships.length);
    const occupied = new Set();
    let nodesVisited = 0;
    const searchLimit = 250000;

    function search(depth) {
      nodesVisited += 1;
      if (nodesVisited > searchLimit) return null;
      if (depth === ships.length) return coversAllHits(fleet, hits);

      const uncoveredHits = new Set([...hits].filter((hit) => !occupied.has(hit)));
      const remainingCapacity = ships.slice(depth).reduce((sum, ship) => sum + ship.length, 0);
      if (uncoveredHits.size > remainingCapacity) return false;

      const candidates = shuffled(candidatesByShip[depth])
        .map((placement) => ({
          placement,
          hitScore: placement.squares.reduce((score, square) => score + (uncoveredHits.has(square) ? 1 : 0), 0),
          noise: Math.random()
        }))
        .sort((a, b) => b.hitScore - a.hitScore || a.noise - b.noise);

      for (const { placement } of candidates) {
        if (placement.squares.some((square) => occupied.has(square))) continue;
        placement.squares.forEach((square) => occupied.add(square));
        fleet[depth] = placement;

        const stillUncovered = [...hits].filter((hit) => !occupied.has(hit));
        const futureCanCover = stillUncovered.every((hit) =>
          candidatesByShip.slice(depth + 1).some((futureCandidates) =>
            futureCandidates.some((candidate) => candidate.squares.includes(hit) && candidate.squares.every((square) => !occupied.has(square)))
          )
        );

        if (futureCanCover && search(depth + 1)) return fleet.slice();
        placement.squares.forEach((square) => occupied.delete(square));
        if (nodesVisited > searchLimit) return null;
      }
      return null;
    }

    return search(0);
  }

  function proposalIsValid(fleet, shipIndex, proposed, hits) {
    const occupiedByOthers = new Set();
    fleet.forEach((placement, index) => {
      if (index !== shipIndex) placement.squares.forEach((square) => occupiedByOthers.add(square));
    });
    if (proposed.squares.some((square) => occupiedByOthers.has(square))) return false;

    if (hits.size > 0) {
      const proposedSet = new Set(proposed.squares);
      for (const hit of hits) {
        if (!occupiedByOthers.has(hit) && !proposedSet.has(hit)) return false;
      }
    }
    return true;
  }

  function validateInput(ships, hits) {
    if (ships.length === 0 && hits.size > 0) return "There are unresolved hits, but no ships are marked as remaining.";
    const totalShipSquares = ships.reduce((sum, ship) => sum + ship.length, 0);
    if (hits.size > totalShipSquares) return `There are ${hits.size} unresolved hits but only ${totalShipSquares} remaining ship squares.`;
    return null;
  }

  function nextFrame() {
    return new Promise((resolve) => requestAnimationFrame(resolve));
  }

  async function simulate() {
    const token = ++simulationToken;
    clearProbabilities();
    runButton.disabled = true;
    const ships = getShips();
    const hits = new Set(boardState.map((state, index) => state === "hit" ? index : -1).filter((index) => index >= 0));
    const forbidden = new Set(boardState.map((state, index) => (state === "miss" || state === "sunk") ? index : -1).filter((index) => index >= 0));
    const inputError = validateInput(ships, hits);
    if (inputError) {
      setStatus(inputError, "error");
      runButton.disabled = false;
      return;
    }

    if (ships.length === 0) {
      setStatus("No ships remain. Every unknown square has probability 0%.", "success");
      renderProbabilities(new Float64Array(CELL_COUNT), 1, ships, hits);
      runButton.disabled = false;
      return;
    }

    setStatus("Checking whether the evidence is consistent…", "running");
    await nextFrame();
    const candidatesByShip = ships.map((ship) => candidatePlacements(ship.length, forbidden));
    if (candidatesByShip.some((candidates) => candidates.length === 0)) {
      setStatus("At least one remaining ship has nowhere it can legally fit.", "error");
      runButton.disabled = false;
      return;
    }

    let fleet = findInitialFleet(ships, candidatesByShip, hits);
    if (!fleet) {
      setStatus("No fleet arrangement fits all of this evidence. Check the hits, misses, sunk squares, and remaining ships.", "error");
      summaryElement.textContent = "The current evidence is inconsistent with the selected remaining fleet.";
      runButton.disabled = false;
      return;
    }

    const targetSamples = Number(sampleCount.value);
    const burnIn = 2500;
    const thinning = 7;
    const totalSteps = burnIn + targetSamples * thinning;
    const counts = new Float64Array(CELL_COUNT);
    let collected = 0;
    let acceptedMoves = 0;

    for (let step = 0; step < totalSteps; step += 1) {
      if (token !== simulationToken) return;
      const shipIndex = Math.floor(Math.random() * ships.length);
      const candidates = candidatesByShip[shipIndex];
      const proposed = candidates[Math.floor(Math.random() * candidates.length)];
      if (proposalIsValid(fleet, shipIndex, proposed, hits)) {
        fleet[shipIndex] = proposed;
        acceptedMoves += 1;
      }

      if (step >= burnIn && (step - burnIn) % thinning === 0) {
        fleet.forEach((placement) => placement.squares.forEach((square) => { counts[square] += 1; }));
        collected += 1;
      }

      if (step % 1800 === 0) {
        const percent = Math.round((step / totalSteps) * 100);
        setStatus(`Simulating legal fleets… ${percent}%`, "running");
        await nextFrame();
      }
    }

    renderProbabilities(counts, collected, ships, hits);
    const acceptanceRate = Math.round((acceptedMoves / totalSteps) * 100);
    setStatus(`Finished ${collected.toLocaleString()} samples · ${acceptanceRate}% of proposed moves accepted.`, "success");
    runButton.disabled = false;
  }

  function renderProbabilities(counts, samples, ships, hits) {
    const probabilities = Array.from(counts, (count) => count / samples);
    const eligible = probabilities
      .map((probability, index) => ({ probability, index }))
      .filter(({ index }) => boardState[index] === "unknown")
      .sort((a, b) => b.probability - a.probability || a.index - b.index);
    const meanProbability = eligible.length
      ? eligible.reduce((sum, item) => sum + item.probability, 0) / eligible.length
      : 0;
    const variance = eligible.length
      ? eligible.reduce((sum, item) => sum + (item.probability - meanProbability) ** 2, 0) / eligible.length
      : 0;
    const standardDeviation = Math.sqrt(variance);
    // Two standard deviations reach the palette endpoints. The 2.5 percentage-
    // point floor prevents a nearly uniform board from amplifying sampling noise.
    const contrastScale = Math.max(2 * standardDeviation, 0.025);

    function mixColor(from, to, amount) {
      const mixed = from.map((channel, index) => Math.round(channel + (to[index] - channel) * amount));
      return `rgb(${mixed.join(", ")})`;
    }

    const neutral = [248, 250, 252];
    const cool = [37, 99, 235];
    const hot = [220, 38, 38];

    cells.forEach((cell, index) => {
      if (boardState[index] !== "unknown") return;
      const probability = probabilities[index];
      const signedContrast = Math.max(-1, Math.min(1, (probability - meanProbability) / contrastScale));
      const intensity = Math.pow(Math.abs(signedContrast), 0.78);
      const heatColor = signedContrast < 0
        ? mixColor(neutral, cool, intensity)
        : mixColor(neutral, hot, intensity);
      cell.classList.add("has-probability");
      cell.style.setProperty("--heat-color", heatColor);
      cell.style.setProperty("--heat-ink", intensity > 0.67 ? "#ffffff" : "#102a43");
      cell.textContent = `${Math.round(probability * 100)}%`;
      cell.setAttribute("aria-label", `${indexToCoordinate(index)}: ${Math.round(probability * 100)} percent estimated occupancy`);
    });

    topTargetsElement.replaceChildren();
    eligible.slice(0, 5).forEach(({ index, probability }) => {
      const item = document.createElement("li");
      item.append(document.createTextNode(indexToCoordinate(index)));
      const percentage = document.createElement("span");
      percentage.textContent = `${(probability * 100).toFixed(1)}%`;
      item.append(percentage);
      topTargetsElement.append(item);
    });

    const shipNames = ships.map((ship) => ship.name).join(", ") || "none";
    summaryElement.textContent = `Based on ${samples.toLocaleString()} sampled fleet arrangements. Remaining ships: ${shipNames}. The ${hits.size} unresolved hit${hits.size === 1 ? " is" : "s are"} required to be covered in every sample. Blue is below the current-board average of ${(meanProbability * 100).toFixed(1)}%; red is above it.`;
  }

  function resetBoard(message = "Board cleared. Enter new evidence, then run the simulation.") {
    simulationToken += 1;
    boardState.fill("unknown");
    clearProbabilities();
    cells.forEach((_, index) => renderCell(index));
    summaryElement.textContent = "Probabilities will appear inside the unknown squares. Blue squares are below the board average, while red squares are above it.";
    setStatus(message, "idle");
    runButton.disabled = false;
  }

  toolButtons.forEach((button) => {
    button.addEventListener("click", () => {
      selectedTool = button.dataset.tool;
      toolButtons.forEach((candidate) => {
        const active = candidate === button;
        candidate.classList.toggle("active", active);
        candidate.setAttribute("aria-pressed", String(active));
      });
    });
  });

  fleetInputs.forEach((input) => input.addEventListener("change", () => {
    simulationToken += 1;
    clearProbabilities();
    summaryElement.textContent = "The remaining fleet changed. Run the simulation to update the probabilities.";
    setStatus("Remaining fleet updated.", "idle");
    runButton.disabled = false;
  }));

  window.addEventListener("pointerup", () => { isPainting = false; });
  window.addEventListener("pointercancel", () => { isPainting = false; });
  clearButton.addEventListener("click", () => resetBoard());
  runButton.addEventListener("click", simulate);
  exampleButton.addEventListener("click", () => {
    resetBoard("Example loaded. Run the simulation to reveal the heatmap.");
    [3, 26, 44, 71, 88].forEach((index) => { boardState[index] = "miss"; });
    [54, 55].forEach((index) => { boardState[index] = "hit"; });
    [12, 13].forEach((index) => { boardState[index] = "sunk"; });
    fleetInputs.forEach((input) => { input.checked = input.dataset.name !== "Destroyer"; });
    cells.forEach((_, index) => renderCell(index));
  });

  initializeBoard();
  const startupWarning = document.getElementById("startup-warning");
  if (startupWarning) startupWarning.hidden = true;
})();
