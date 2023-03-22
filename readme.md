# ODL Intake
This toolbox provides a set of preset functions that can open various, cloud based, Ocena Data Lab data products

## Saving access keys as environmental variable
Often access keys are required to gain access to the datasets. These should be saved as environment variables. Here's how to do that. These instructions are for computers running linux and using bash for their terminal.

- Open configuration file
``` nano ~/.bashrc```

- add the following lines
```
# >>> add access tokens >>>#
export <variable name>="<variable value>"``` (spaced matter, there shouldn't be a space before or after the equal sign)

# you can add other access tokens here 
.
.
.

# <<< add access tokens>>>
```
