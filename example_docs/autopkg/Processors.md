A processor is a [python class](https://docs.python.org/3/tutorial/classes.html) which may be called upon by AutoPkg recipes to perform specific tasks. Every task in an AutoPkg recipe calls a processor. Each class is situated in its own [python module](https://docs.python.org/3/tutorial/modules.html) (i.e. file). Most (but not all) processors require arguments which may come from the running environment or be defined in the recipe. Some (but not all) processors output variables to the running environment for use by subsequent processes in the same AutoPkg recipe or a child recipe.

AutoPkg ships with a bunch of processors which can be used to perform many of the commonly required tasks in recipes. A description of each of these processors is provided in the **Processor Reference** list in this wiki. 

Some recipes have their own custom processor to solve a problem specific to the item that is being processed. 

There are also a lot of third-party processors which can be called upon for use cases beyond those provided by the processors that ship with AutoPkg. 

**See also:**

* [Recipe Format ≫ process](Recipe-Format#process)
* [Processor Locations](Processor-Locations) 
* [Noteworthy Third Party Processors](Noteworthy-Processors)
* [Developing Custom Processors](Developing-Custom-Processors)