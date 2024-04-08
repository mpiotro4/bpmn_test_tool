Scenario: scenario 0
Given Then User wants to create a new task
When Create new task
Then Priority of the task priority = ? 
When Assign to high priority queue priority = high 
Then Priority assigned
When task created

Scenario: scenario 1
Given Then User wants to create a new task
When Create new task
Then Priority of the task priority = ? 
When Assign to low priority queue priority = low 
Then Priority assigned
When task created

