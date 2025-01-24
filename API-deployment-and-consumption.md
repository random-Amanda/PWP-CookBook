# Important information for Deadline 5


:bangbang:&nbsp;&nbsp;**This chapter should be completed by Deadline 5** *(see course information at [Lovelace](http://lovelace.oulu.fi))*

---
<details>
<summary>
:bookmark_tabs:&nbsp;&nbsp;<strong>Chapter summary</strong>
</summary>

<bloquote>
In this section your group must design, implement and test a client application that uses the RESTful API implemented by you. If you utilize HTML and JavaScript, it is mandatory that the HTML is contained in static files. It means that your server cannot generate HTML dynamically (using PHP or JSP).  All modifications made to the webpage must be done in the client side using javascript. Of course,  you can use anchors (<a>) to load a new URL. Please, consider  the <a href="http://en.wikipedia.org/wiki/Same_origin_policy">Same Origin Policy"</a>  because it might cause problems to your client implementation. It is recommend to host the files in a local HTTP server and not directly in your file system. We will give you more instructions in Exercise 4. 

In addition, you can either

* Include an auxiliary service that interacts with your API (and possibly the client). More information in Exercise 4.
* Deploy your web api in a production environment, as explained in Exercise 3

</strong>
<h3>CHAPTER GOALS</h3>
<ul>
<li>Deploy an API in a production environment </li>
<li>Learn how to use APIs</li>
<li>Implement a client that uses the project API</li>
<li>Implement an auxiliary service that interacts with your API</li>
</ul>
</bloquote>

</details>

---

<details>
<summary>
:heavy_check_mark:&nbsp;&nbsp;&nbsp;&nbsp; <strong>Chapter evaluation (max 26 points)</strong>
</summary>

<bloquote>
You can get a maximum of 26 points after completing this section. You can check more detailed assessment criteria in the Lovelace return box for Deadline 5. 
</bloquote>

</details>

---

# RESTful Client


## Client application description
### Overview
<details>
<summary>
:bookmark_tabs:&nbsp;&nbsp;<strong>Content that must be included in the section</strong>
</summary>

<bloquote>
You must provide a description of the application. You must clarify which are the goals of the application and why a user would like to use this application. <strong>You must also state what is the functionality provided by the RESTful API used by this application.</strong>


</bloquote>

</details>

---
:pencil2: *Write here your application description*

---

### Functional requirements

<details>
<summary>
:bookmark_tabs:&nbsp;&nbsp;<strong>Content that must be included in the section</strong>
</summary>

<bloquote>
Provide a use case diagram of your application. For each case, specify which is the API resource/s that cover the given functionality

</bloquote>

</details>

---


:pencil2: *Draw your diagram here including a discussion of use cases*

---


## Client design
### GUI layout

<details>
<summary>
:bookmark_tabs:&nbsp;&nbsp;<strong>Content that must be included in the section</strong>
</summary>

<bloquote>
Draw a diagram of the client layout. Students can use any software they want to do the sketching. For more professional-like design, students can use any wireframing tool available in Internet. Some of them can be found from <a href="https://www.hostinger.com/tutorials/best-wireframing-tools">https://www.hostinger.com/tutorials/best-wireframing-tools</a>. <a href="http://pencil.evolus.vn/Default.html">Pencil </a>is free, open source and easy to use. Other options are Visio and Balsamiq (you need a license). You can also create the UI using a paper and a pencil and scan the resulting drawing.
</bloquote>

</details>

---

:pencil2: *Add your diagrams here*

---

### Screen workflow

<details>
<summary>
:bookmark_tabs:&nbsp;&nbsp;<strong>Content that must be included in the section</strong>
</summary>

<bloquote>
Draw the screen workflow of your client (which are the possible screens that you can access from one specific screen?)

</bloquote>

</details>

---

:pencil2: *Add your diagrams here*

## Client implementation

<details>
<summary>
:computer:&nbsp;&nbsp;&nbsp;&nbsp; <strong>TODO: SOFTWARE TO DELIVER IN THIS SECTION</strong>
</summary>

<bloquote>
<strong>The code repository must contain: </strong>
<ol>
	<li>The source code for the client application.&nbsp;</li>
	<li>External libraries. You can also report them in the <a href="doc/README.md">README.md</a> if the libraries are very big or need to be installed.</li>
	<li>The code for testing the application (if it exists).</li>
	<li>We recommend to include a set of scripts to run your application and tests (if they exist).</li>
	<li>A <a href="doc/README.md">README.md</a> file containing:
		<ul>
			<li>Dependencies (external libraries)</li>
			<li>How to setup/install the client</li>
			<li>How to configure and run the client</li>
			<li>How to run the different tests of your client (if you have implemented unit testing)</li>
		</ul>
	</li>
</ol>
<strong>NOTE: Your code MUST be clearly documented. </strong>For each public method/function you must provide: a short description of the method, input parameters, output parameters, exceptions (when the application can fail and how to handle such fail). Check Exercise 4 for examples on how to document the code.
<strong> addition, should be clear which is the code you have implemented yourself and which is the code that you have borrowed from other sources.</strong>
</bloquote>

</details>

---

:pencil2: *Implement your client and include a few screenshots of the final version of the client to show that meets the requirements*

---


# Auxiliary Service

Please, note that if you are deploying your WEB API as instructed in Exercise 3, you do not need to complete this task. 


## Service description
### Overview
<details>
<summary>
:bookmark_tabs:&nbsp;&nbsp;<strong>Content that must be included in the section</strong>
</summary>

<bloquote>
You must provide a description of the service. You must clarify which are the goals of the service and how it interacts with your API (and possibly the client). The service can be autonomous entity that does some automated work on the API (data cleaning, calculating composites etc.), or it can be commanded from the client interface to perform heavier tasks that would clog the API server itself (statistics generation, recommendation algorithms etc.). 


</bloquote>

</details>

---

:pencil2: *Write your description here*

---

### Functional requirements

<details>
<summary>
:bookmark_tabs:&nbsp;&nbsp;<strong>Content that must be included in the section</strong>
</summary>

<bloquote>
Provide a diagram that shows how the service communicates with other parts in the ecosystem.

</bloquote>

</details>

---

:pencil2: *Put your diagram here*

---
## Auxiliary service implementation

<details>
<summary>
:computer:&nbsp;&nbsp;&nbsp;&nbsp; <strong>TODO: SOFTWARE TO DELIVER IN THIS SECTION</strong>
</summary>

<bloquote>
<strong>The code repository must contain: </strong>
<ol>
	<li>The source code for the auxiliary service.&nbsp;</li>
	<li>External libraries. You can also report them in the <a href="doc/README.md">README.md</a> if the libraries are very big or need to be installed.</li>
	<li>The code for testing the service (if it exists).</li>
	<li>We recommend to include a set of scripts to run your service and tests (if they exist).</li>
	<li>A <a href="doc/README.md">README.md</a> file containing:
		<ul>
			<li>Dependencies (external libraries)</li>
			<li>How to setup/install the service</li>
			<li>How to configure and run the service</li>
			<li>How to run the different tests of your service (if you have implemented unit testing)</li>
		</ul>
	</li>
</ol>
<strong>NOTE: Your code MUST be clearly documented. </strong>For each public method/function you must provide: a short description of the method, input parameters, output parameters, exceptions (when the application can fail and how to handle such fail). Check Exercise 4 for examples on how to document the code.
<strong> Should be clear which is the code you have implemented yourself and which is the code that you have borrowed from other sources.</strong>
</bloquote>

</details>

---

:pencil2: *Do not need to write anything here. Implement your service*

---

# Web API production deployment

**NOTE: This section might have significant changes along the course, please stay tunned to possible modifications. They will be discussed in Discord / Lovelace**

Please, note that if you are creating an auxiliary service, you do not need to complete this task. 


## Deployment architecture
### Overview
<details>
<summary>
:bookmark_tabs:&nbsp;&nbsp;<strong>Content that must be included in the section</strong>
</summary>

<bloquote>
You must provide an architecture diagram of the system ready for production deployment, including all the different components as well as their connections. 


</bloquote>

</details>

---

:pencil2: *Add your diagram here*

---

### Tools description

<details>
<summary>
:bookmark_tabs:&nbsp;&nbsp;<strong>Content that must be included in the section</strong>
</summary>

<bloquote>
List all components you are using and a description of the role and functionality that this component has in the system. Explain why this component is necessary for and list alternatives. 

</bloquote>

</details>

---

:pencil2: *Add your text here*

---

## Deployment

<details>
<summary>
:computer: Content that must be included in this section
</summary>

<bloquote>
You must deploy the Wep API in environment similar to the one proposed in Exercise 3 and show that is working
&nbsp;&nbsp;&nbsp;&nbsp; <strong>TODO: SOFTWARE TO DELIVER IN THIS SECTION</strong>
<strong>The code repository must contain: </strong>
<ol>
	<li>Scripts needed to setup the environment and deploy the web apit&nbsp;</li>
	<li>Software needed to create and maintain the certificates </li>
	<li>A <a href="doc/README.md">README.md</a> file containing:
		<ul>
			<li>List of components that must be installed</li>
			<li>How to setup the environment</li>
			<li>How to deploy the web api into the environment</li>
			<li>How to run the different tests to check that your environment is properly configure</li>
		</ul>
	</li>
</ol>
<strong> Should be clear which is the code you have implemented yourself and which is the code that you have borrowed from other sources.</strong>
</bloquote>

</details>

---

:pencil: *Do not need to write anything here. Deploy your API and include all necessary files in the repository*

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