---
layout: page
title: Battleship Probability Lab
permalink: /code/heatmap/battleship-heatmap
---

<link rel="stylesheet" href="./battleship.css">

<main class="battleship-app" id="battleship-app">
  <header class="hero">
    <p class="eyebrow">Math 180 · Monte Carlo Lab</p>
    <h1>Battleship Probability Lab</h1>
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
        <span>Lower probability</span>
        <span class="gradient" aria-hidden="true"></span>
        <span>Higher probability</span>
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

  <section class="results-card" aria-labelledby="results-heading">
    <div>
      <p class="step-label">Step 3</p>
      <h2 id="results-heading">Interpret the estimate</h2>
      <p id="summary">Probabilities will appear inside the unknown squares. They estimate the chance that each square is occupied by one of the ships still afloat.</p>
    </div>
    <ol class="top-targets" id="top-targets" aria-label="Highest probability targets"></ol>
  </section>

  <details class="method-card">
    <summary>How does the simulation work?</summary>
    <div class="method-copy">
      <p>The program first finds a legal placement of the selected ships. Ships are horizontal or vertical, cannot overlap, and may touch. Every unresolved hit must lie on a remaining ship; misses and sunk squares cannot.</p>
      <p>It then repeatedly proposes moving one ship to a randomly selected legal position. Moves inconsistent with the evidence are rejected. After a warm-up period, the program records many fleet arrangements and reports the fraction that occupy each square. This is a Monte Carlo estimate, so rerunning it may change the percentages slightly.</p>
      <p><strong>Modeling question:</strong> Does treating every legal fleet arrangement as equally plausible match how a real opponent chooses positions?</p>
    </div>
  </details>
</main>

<noscript>This activity requires JavaScript to run.</noscript>

<script src="./battleship.js" defer></script>

