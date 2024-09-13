# test-voila-notebook

# Drag and Drop Example

<p>Drag the items into the correct box:</p>

<div style="display:flex; gap: 20px;">
  <div id="dragItems" style="border:1px solid #000; padding:10px; width:150px;">
    <p id="item1" draggable="true" ondragstart="drag(event)">Item 1</p>
    <p id="item2" draggable="true" ondragstart="drag(event)">Item 2</p>
    <p id="item3" draggable="true" ondragstart="drag(event)">Item 3</p>
  </div>

  <div id="dropZone" style="border:1px solid #000; padding:10px; width:150px;" ondrop="drop(event)" ondragover="allowDrop(event)">
    <p>Drop Here</p>
  </div>
</div>

<script>
  function allowDrop(ev) {
    ev.preventDefault();
  }

  function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
  }

  function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    ev.target.appendChild(document.getElementById(data));
  }
</script>
