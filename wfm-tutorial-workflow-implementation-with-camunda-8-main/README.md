# Workflow Implementation With Camunda 8
The tutorial **Workflow Implementation With Camunda 8** introduces some Camunda 8 features that can be used to implement a workflow. This repository contains all resources used in this tutorial.

## Resources 
The following BPMNs, DMNs, source code folders, ect.., are used in the tutorial. The vegetable icons are the reference from the tutorial slides.

### 🍅 Baseline Model
- [Baseline BPMN Model](./1_BaselineModel.bpmn) (Final Model from the last tutorial)
    - [Define Work Form](./1.1_DefineWork.form)
    - [Do Simple Work Form](./1.2_DoSimpleWork.form)
    - [Do Hard Work Form](./1.3_DoHardWork.form)

### 🥑 Service Task with a Python Worker
- [BPMN Model with Service Task with Python Worker](./2_ModelWithMoodCalculator.bpmn)
- [python-worker](./python-worker) (The python worker source code)

### 🧅 Business Rule Task with DMN
- [BPMN Model with a Business Rule Task](./3_ModelWithDMNTaskHardWork.bpmn)
- [DMN Model](3_DMN.dmn) (The DMN model used in the BPMN)

### 🥕 Service Task with a FEEL Script
- [BPMN Model with Service Task with FEEL](./4_ModelWithServiceTaskSimpleWork.bpmn)


### 🫐 Connector Task (REST)
- [BPMN Model with a Connector Task (REST)](./5_ModelWithConnectorRESTTask.bpmn)
- [Updated Define Work Form](./5.1_DefineWork.form)
