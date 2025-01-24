# Important information for Deadline 4


:bangbang:&nbsp;&nbsp;**This chapter should be completed by Deadline 4** *(see course information at [Lovelace](http://lovelace.oulu.fi))*

---
<details>
<summary>
:bookmark_tabs:&nbsp;&nbsp;<strong>Chapter summary</strong>
</summary>

<bloquote>
In this chapter, the students&nbsp;<strong>must modify their API to use hypermedia following REST principles and document their RESTful API. The minimum requirements are summarized in the&nbsp;<a href="https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/pwp-project-work-assignment/#minimum-requirements-and-constraints">Minimum Requirements</a>&nbsp;section of the Project Work Assignment. Note that if you do not meet Minimum Requirements this section wont be evaluated.</strong>

<h3>SECTION GOALS: </h3>
<ul>
<li>Understand connectedness and/or hypermedia</li>
<li>Write API documentation</li>
</ul>

<p>
	You have two options:
		<ol>
			<li>Implement the API using a non-hypermedia format (RESTful CRUD). In this case, it is recommended that all your resources are connected (linking to other resources). <strong>Anyhow, you cannot get full points in this section if you do not design your API using an hypermedia format</strong></li>
			<li>Using an hypermedia format. Lots of examples provided in Exercise 3. You can get full points. In this case you need to clearly include in the documentation a profile with link relations and semantic descriptors.</li>
		</ol>

</p>

</details>

---
<details>
<summary>
:heavy_check_mark:&nbsp;&nbsp;&nbsp;&nbsp; <strong>Chapter evaluation (max 18 points)</strong>
</summary>

<bloquote>
You can get a maximum of 18 points after completing this section. More detailed evaluation is provided in the evaluation sheet in Lovelace.
</bloquote>

</details>

---

# Hypermedia
## Resource relations
<details>
<summary>
:bookmark_tabs:&nbsp;&nbsp;<strong>Content that must be included in the section</strong>
</summary>

<bloquote>
Include a state diagram of your application, with all the application states. Each resource must be an application state. Describe also the state transitions. To build this diagram you should reuse the diagram created in DL1. You can use online tools such as <a href="https://www.draw.io/">draw.io or <a href="https://www.lucidchart.com/">lucidchart</a> to create the diagrams. You have an example in the following image

<img src="uploads/448d6edbd82d4784e9aff04dcbb1c60c/Forum_state_diagram.png"></img>

</bloquote>

</details>

---

:pencil2: *Draw here your state machine diagram*

---
## Hypermedia implementation 

<details>
<summary>
:computer:&nbsp;&nbsp;&nbsp;&nbsp; <strong>TODO: SOFTWARE TO DELIVER IN THIS SECTION</strong>
</summary>

<bloquote>
<strong>The code repository must contain: </strong>
<ol>
	<li>The source code of the RESTful API incorporating hypermedia. The source coude should be documented using the same quality criteria in Deliverable 3. Please, remember to include original source if you have not written the code (even if you have used an AI).</li>
	<li>Necessary scripts to run your server</li>
	<li>The README.md file with all the information described in the Deliverable 3. </li>
</ol></bloquote>

</details>

---
:pencil2: *You do not need to write anything in this section, just complete the implementation.*

---

### RESTful API testing using hypermedia
<details>
<summary>
:computer:&nbsp;&nbsp;&nbsp;&nbsp; <strong>TODO: SOFTWARE TO DELIVER IN THIS SECTION</strong>
</summary>

<bloquote>
<strong>The code repository must contain: </strong>
<ol>
	<li>The code to test your RESTful API (Functional test)
		<ul>
			<li>The code of the test MUST be commented indicating what you are going to test in each test case.</li>
			<li>The test must include values that force error messages</li>
		</ul>
	</li>
	<li>The external libraries that you have used</li>
	<li>We recommend to include a set of scripts to execute your tests.</li>
	<li>A database file or the necessary files and scripts to automatically populate your database.</li>
	<li>A <a href="documents/README.md">README.md</a> file containing:
		<ul>
			<li>Dependencies (external libraries)</li>
			<li>Instructions on how to run the different tests for your application.</li>
		</ul>
	</li>
</ol>
Do not forget to include in the <a href="doc/README.md">README.md</a> the instructions on how to run your tests. Discuss briefly which were the main errors that you detected thanks to the functional testing.

Remember that you MUST implement a functional testing suite. A detailed description of the input / output in the a REST client plugin.

In this section it is your responsibility that your API handles requests correctly. All of the supported methods for each resource should work. You also need to show that invalid requests are properly handled, and that the response codes are correct in each situation.
</bloquote>

</details>

---
:pencil2: *Most important part of this section is completing the implementation. Write down here a short reflection on  the main errors you have solved thanks to the functional tests.*

---
## Justification on Hypermedia Implementation

<details>
<summary>
:bookmark_tabs:&nbsp;&nbsp;<strong>Content that must be included in this section. Fill this section if your API uses hypermedia</strong>
</summary>

<bloquote>
Declare your chosen mediatype, and provide your reasoning for choosing that mediatype. For each custom link relation defined in your API's namespace, explain why it was needed (i.e. why there wasn't a suitable relation in the IANA standard). Explain how Connectedness is achieved in your API.
</bloquote>
</details>

---

:pencil2: <em>Write your text here </em>


---

# RESTful API documentation

## API Documentation

<details>
<summary>
:bookmark_tabs:&nbsp;&nbsp;<strong>Content that must be included in the section</strong>
</summary>

<bloquote>
<p>Use any of the tools presented in Exercise 3 to document the API. 

For all resources you must cover:
<ul>
<li>The possible HTTP methods exposed by this resource</li>
<li>The headers in the request and responses</li>
<li>The media type utilized (in the response Content-Type header). If you are utilizing your own media-type you must describe it in the section Own media type implementation.</li>
<li>The format of the HTTP request body (just for PUT/POST), providing a clear example. If necessary, comment the example.</li>
<li>The format of the HTTP response body, providing a clear example. If necessary, comment the example.</li>
<li>The error conditions, status code and format of the error response, providing a clear example.</li>
<li><em>If you are using an hypermedia type you must provide the profile utilized, including:</em> 
<ul>
<li>Link relations. Include methods and format of the requests if they are defined in the media type. Use as much as possible IANA defined relations.</li>
<li>Semantic descriptors. If you utilize a descriptor used in some other profile (e.g. <a href="http://schema.org/docs/schemas.html">schema.org</a>) provide the link. </li>
<li>If you are extending other profiles, do not forget to link to the extended profile.</li></ul></li>
</ul>

</bloquote>

</details>

---


:pencil2: <em>Put the link to your API documentation here</em>


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
