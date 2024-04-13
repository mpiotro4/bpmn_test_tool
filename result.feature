Scenario: scenario 0
Given Then start
When user task
Then gateway 1 option = ? 
When service task 1 option = one 
Then gateway 4
When end

Scenario: scenario 1
Given Then start
When user task
Then gateway 1 option = ? 
When service task 2 option = two 
Then gateway 2 option = ? 
When service task 4 option = two 
Then gateway 3
When gateway 4
Then end

Scenario: scenario 2
Given Then start
When user task
Then gateway 1 option = ? 
When service task 2 option = two 
Then gateway 2 option = ? 
When service task 3 option = one 
Then gateway 3
When gateway 4
Then end

