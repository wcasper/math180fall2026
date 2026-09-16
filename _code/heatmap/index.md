---
layout: page
title: Battleship Heatmap
permalink: /code/heatmap/battleship-heatmap
---

<link rel="stylesheet" href="./battleship.css">

<div class="startup-warning" id="startup-warning">
  The page loaded, but <code>battleship.js</code> did not start. Confirm that
  this Markdown file, <code>battleship.js</code>, and <code>battleship.css</code>
  are in the same folder, with matching capitalization.
</div>

<main class="battleship-app" id="battleship-app">
  <header class="hero">
    <p class="lede">Record what you know, then simulate fleets that fit the evidence. The heatmap estimates where the remaining ships are most likely to be.</p>
  </header>

  <section class="control-card" aria-labelledby="record-heading">
    <div class="section-heading">
      <div>
        <p class="step-label">Step 1</p>
        <h2 id="record-heading">Record the board</h2>
      </div>
      <button class="quiet-button" id="clear-board" type="button">Clear board</button>
    </div>

    <div class="tools" role="toolbar" aria-label="Board marking tools">
      <button class="tool-button active" type="button" data-tool="unknown" aria-pressed="true">
        <span class="tool-swatch unknown-swatch" aria-hidden="true"></span>Unknown
      </button>
      <button class="tool-button" type="button" data-tool="miss" aria-pressed="false">
        <span class="tool-swatch miss-swatch" aria-hidden="true"></span>Miss
      </button>
      <button class="tool-button" type="button" data-tool="hit" aria-pressed="false">
        <span class="tool-swatch hit-swatch" aria-hidden="true"></span>Unresolved hit
      </button>
      <button class="tool-button" type="button" data-tool="sunk" aria-pressed="false">
        <span class="tool-swatch sunk-swatch" aria-hidden="true"></span>Sunk ship
      </button>
    </div>

    <p class="hint">Choose a tool, then click or drag across squares. A sunk square is treated as unavailable to the remaining fleet.</p>
  </section>

  <div class="workspace">
    <section class="board-card" aria-label="Battleship board and probability heatmap">
      <div class="board-shell">
        <div class="corner-label" aria-hidden="true"></div>
        <div class="column-labels" id="column-labels" aria-hidden="true"></div>
        <div class="row-labels" id="row-labels" aria-hidden="true"></div>
        <div class="board" id="board" role="grid" aria-label="10 by 10 Battleship board"></div>
      </div>
      <div class="legend" aria-label="Probability color scale">
        <span>Below average</span>
        <span class="gradient" aria-hidden="true"></span>
        <span>Above average</span>
      </div>
    </section>

    <aside class="settings-card" aria-labelledby="fleet-heading">
      <p class="step-label">Step 2</p>
      <h2 id="fleet-heading">Set the remaining fleet</h2>
      <p class="small-copy">Uncheck a ship after it has sunk. Mark its occupied squares as <strong>Sunk ship</strong> on the board.</p>

      <div class="fleet-list" id="fleet-list">
        <label><input type="checkbox" value="5" data-name="Carrier" checked> <span>Carrier</span><b>5</b></label>
        <label><input type="checkbox" value="4" data-name="Battleship" checked> <span>Battleship</span><b>4</b></label>
        <label><input type="checkbox" value="3" data-name="Cruiser" checked> <span>Cruiser</span><b>3</b></label>
        <label><input type="checkbox" value="3" data-name="Submarine" checked> <span>Submarine</span><b>3</b></label>
        <label><input type="checkbox" value="2" data-name="Destroyer" checked> <span>Destroyer</span><b>2</b></label>
      </div>

      <label class="select-label" for="sample-count">Number of sampled fleets</label>
      <select id="sample-count">
        <option value="1000">1,000 · quick</option>
        <option value="5000" selected>5,000 · balanced</option>
        <option value="20000">20,000 · smoother</option>
      </select>

      <button class="run-button" id="run-simulation" type="button">Estimate probabilities</button>
      <button class="example-button" id="load-example" type="button">Load an example board</button>

      <div class="status idle" id="status" role="status" aria-live="polite">
        Enter some evidence, then run the simulation.
      </div>
    </aside>
  </div>
</main>

<noscript>This activity requires JavaScript to run.</noscript>
<script src="./battleship.js" defer></script>
