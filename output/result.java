@Test
public void scenario1() {
	final ProcessInstance instance = runtimeService().startProcessInstanceByKey("Process_084wgog");
	assertThat(instance).isStarted();
	assertThat(instance).isWaitingAt("user-task");
	
	Map<String, Object> variables = new HashMap<>();
    variables.put("option", "one");
    complete(task(), variables);
	
	assertThat(instance).hasPassed("end").isEnded();
}

@Test
public void scenario2() {
	final ProcessInstance instance = runtimeService().startProcessInstanceByKey("Process_084wgog");
	assertThat(instance).isStarted();
	assertThat(instance).isWaitingAt("user-task");
	
	Map<String, Object> variables = new HashMap<>();
    variables.put("option", "two");
    complete(task(), variables);
	
	Map<String, Object> variables = new HashMap<>();
    variables.put("option", "two");
    complete(task(), variables);
	
	
	assertThat(instance).hasPassed("end").isEnded();
}

@Test
public void scenario3() {
	final ProcessInstance instance = runtimeService().startProcessInstanceByKey("Process_084wgog");
	assertThat(instance).isStarted();
	assertThat(instance).isWaitingAt("user-task");
	
	Map<String, Object> variables = new HashMap<>();
    variables.put("option", "two");
    complete(task(), variables);
	
	Map<String, Object> variables = new HashMap<>();
    variables.put("option", "one");
    complete(task(), variables);
	
	
	assertThat(instance).hasPassed("end").isEnded();
}

