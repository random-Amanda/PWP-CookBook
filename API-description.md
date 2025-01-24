# Important information for Deadline 1


:bangbang:&nbsp;&nbsp;**This chapter should be completed by Deadline 1** *(see course information at [Lovelace](http://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/))*

---
<details>
<summary>
:bookmark_tabs:&nbsp;&nbsp;<strong>Chapter summary</strong>
</summary>

<bloquote>
This chapter must provide a good overview of the Web API that your group is going to develop during the course, and some insight into the (imaginary) microservice architecture it will be a part of. You should not focus in implementation aspects such as database structure,  interfaces or the request/responses formats. We recommend that you look into existing APIs (see Related work below) before writing the description for your own API.

<h3>Chapter GOALS:</h3>
<ol>
<li>Understand what is an API</li>
<li>Describe the project topic API</li>
<li>Describe how the API would be used as part of a larger architecture</li>
</ol>
</bloquote>

</details>

---

<details>
<summary>
:heavy_check_mark:&nbsp;&nbsp;&nbsp;&nbsp; <strong>Chapter evaluation (max 5 points)</strong>
</summary>

<bloquote>
You can get a maximum of 5 points after completing this Chapter. More detailed evaluation is provided in the evaluation sheet in Lovelace.
</bloquote>

</details>

---

# RESTful API description
## Overview
<details>
<summary>
:bookmark_tabs:&nbsp;&nbsp;<strong>Content that must be included in the section</strong>
</summary>

<bloquote>

Describe the API you are going to implement. Also describe the larger imaginary architecture that would exist around that API - while you do not need to implement these other components, they will be helpful in imagining context for your API. Your API will be a component that stores, and offers an interface to, some important data in the larger ecosystem. Think about a larger system, and then take out one key piece to examine - this will be your API.

Describe the API briefly and comment what is the main functionality that it exposes. Focus in the API not in any specific application that is using this API. Take into account that in the end, a WEB API is an encapsulated functionality as well as the interface to access that functionality. Remember that your API is just one part of a larger machine. It does not need to do everything. There will be other components in the system to do those things. This course focuses on creating a small API in detail - thinking too big from the start will drown you in work later. 

A really short version of an overview for the RESTful Web API could be: 

<em>“The discussion forum Web API offers different functionalities to structure non-real-time conversations among the people of a group about topics they are interested in certain topic. Messages are grouped in Threads, that at the same time are grouped in Topics. The messages are accessible to anyone, but posts can only be created by providing credentials of a registered user [...] This API could exist as part of an online learning environment system where it is responsible for offering discussion forum features that can be included in other components of the learning environment. For example, a programming task (managed by a different component) can include its own discussion board managed by the discussion forum API[...]“</em>

</bloquote>

</details>

---

:pencil2: *Write your description here*

---


## Main concepts and relations
<details>
<summary>
:bookmark_tabs:&nbsp;&nbsp;<strong>Content that must be included in the section</strong>
</summary>

<bloquote>
<strong>Define</strong> the <strong>main concepts</strong> and describe the <strong>relations</strong> among them textually. Roughly, a concept is a real-world entity that is expected to be of interest to users or other services. This section will be a guideline for choosing your resources to implement in Deadline 3. Students should remember that some of the concepts might not be a resource by themselves, but just a part of it (resource property). In this section, students should not describe the RESTful resources, but identify which are the main ideas of the API. Do not forget to include the relations among the concepts.

A description of the main concepts for the Forum API could be: 

<em>"The API permits users send messages. The forum contains a list of categories and a list of users. Each category specifies a name, a description and a thread. A thread is [...]The forum may contain 0 or more categories… Each category may have 0 or more threads… Users can write and read messages to a forum thread. A user has a profile, basic information, activity information (stores, for instance, all the messages sent by a user, the messages marked as favorites). [...]The user history contains information of the last 30 messages sent by the user.[…]"</em>

Include a diagram which shows the relations among concepts.

This section is important because it outlines the concepts that you will later implement. In particular, the diagram defined here will follow you throughout the project report and you will be adding more details to it. 


</bloquote>

</details>

---

:pencil2: *Write your text here and draw the diagram*

---

## API uses
<details>
<summary>
:bookmark_tabs:&nbsp;&nbsp;<strong>Content that must be included in the section</strong>
</summary>

<bloquote>
Describe at least one client and one service that could use your Web API. You must explain here what is the functionality provided by the client/service, and how it uses the Web API to implement this functionality. 
</bloquote>

</details>

---

:pencil2: *Write your text here*



## Related work
<details>
<summary>
:bookmark_tabs:&nbsp;&nbsp;<strong>Content that must be included in the section</strong>
</summary>

<bloquote>
Find at least one API that resembles the functionality provided by yours. Explain in detail the functionality provided by the API. Classify the API according to its type (RPC, CRUD REST, pure REST, hypermedia driven ...) justifying your selection. Provide at least one example client that uses this API.

The purpose of this task is to get more familiar with what an API is. This will be helpful in describing your own API. Therefore, it is recommended to do this section after you have decided the topic of your project but before writing your API description.
</bloquote>

</details>

---



:pencil2: *Write your text here*

---

## Use of AI

---

:pencil: If you have use AI during this deliverable, explain what tool/s you have used and how. 

---


## Resources allocation
|**Task** | **Student**|**Estimated time**|
|:------: |:----------:|:----------------:|
|||| 
|||| 
|||| 
|||| 
|||| 