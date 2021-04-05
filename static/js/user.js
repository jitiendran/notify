const task = document.getElementById("tasks");

// const taskArray = task.dataset.tasks.split(",");
let taskArray = task.dataset.tasks;
taskArray = taskArray.slice(1);
taskArray = taskArray.slice(0, taskArray.length - 1);
const Arrays = taskArray.split(",");
console.log(typeof Arrays);

for (let i = 0; i < Arrays.length; i++) {
  console.log(Arrays[i]);
  task.innerHTML += `<div class="task-content">
    <p>${i + 1}</p>
    <p>${Arrays[i].replace(/^'|'$/g, "")}</p>
  </div>`;
}
