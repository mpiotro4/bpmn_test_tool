@Test
public void scenario1() {
    final ProcessInstance instance = runtimeService().startProcessInstanceByKey("camunda_task_process");

    assertThat(instance).isWaitingAt("create-new-task");

    Map<String, Object> variables = new HashMap<>();
    variables.put("priority", "low");
    variables.put("description", "xD");
    variables.put("taskName", "xD");
    complete(task(), variables);

    assertThat(instance)
            .hasPassed("assign-low");

    assertThat(instance)
            .hasPassed("task-created")
            .isEnded();
}

@Test
public void scenario2() {
    final ProcessInstance instance = runtimeService().startProcessInstanceByKey("camunda_task_process");

    assertThat(instance).isWaitingAt("create-new-task");

    Map<String, Object> variables = new HashMap<>();
    variables.put("priority", "high");
    variables.put("description", "xD");
    variables.put("taskName", "xD");
    complete(task(), variables);

    assertThat(instance)
            .hasPassed("assign-high");

    assertThat(instance)
            .hasPassed("task-created")
            .isEnded();
}