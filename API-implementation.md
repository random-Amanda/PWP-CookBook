# Important information for Deadline 3


:bangbang:&nbsp;&nbsp;**This chapter should be completed by Deadline 3** *(see course information at [Lovelace](http://lovelace.oulu.fi))*

---
<details>
<summary>
:bookmark_tabs:&nbsp;&nbsp;<strong>Chapter summary</strong>
</summary>

<bloquote>
In this section you must implement a RESTful API. <strong>The minimum requirements are summarized in the&nbsp;<a href="https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/pwp-project-work-assignment/#minimum-requirements-and-constraints">Minimum Requirements</a>&nbsp;section of the Project Work Assignment. If you do not meet the minimum requirements this section WILL NOT be evaluated. </strong>
<h3>CHAPTER GOALS</h3>
<ul>
<li>Implement a RESTful API</li>
<li>Write tests for the API</li>
</ul>
</bloquote>

</details>

---
<details>
<summary>
:heavy_check_mark:&nbsp;&nbsp;&nbsp;&nbsp; <strong>Chapter evaluation (max 21 points)</strong>
</summary>

<bloquote>
You can get a maximum of 21 points after completing this section. More detailed evaluation is provided in the evaluation sheet in Lovelace.
</bloquote>

</details>

---

# RESTful API implementation

## List of implemented resources

<details>
<summary>
:bookmark_tabs:&nbsp;&nbsp;<strong>Content that must be included in the section</strong>
</summary>

<bloquote>
A list of all resourcess. Each resource should include its URL, a short description and supported methods. You should mark also which is the name of the class implementing the resource (if you have implemented such resource) Consider that you do not need to implement every resource you initially planned. &nbsp; The minimum requirements are summarized in the <a href="https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/pwp-project-work-assignment/#minimum-requirements-and-constraints">Minimum requirements section</a> from the Project work assignment. 

</bloquote>

</details>

---

:pencil2: *List your resources here. You can use the table below for listing resources. You can also list unimplemented resources if you think they are worth mentioning*

|  Resource name       | Resource url | Resource description | Supported Methods    | Implemented |
|:-------------------: |:------------:|:--------------------:|:--------------------:|:-----------:|
|Resource Name 1       |              |                      |                      |             |
|Resource Name 2       |              |                      |                      |             |

---

## Basic implementation
<details>
<summary>
:computer:&nbsp;&nbsp;&nbsp;&nbsp; <strong>TODO: SOFTWARE TO DELIVER IN THIS SECTION</strong>
</summary>

<bloquote>
<strong>The code repository must contain: </strong>
<ol>
	<li>The source code for the RESTful API&nbsp;</li>
	<li>The external libraries that you have used</li>
	<li>We recommend to include a set of scripts to setup and run your server </li>
	<li>A database file or the necessary files and scripts to automatically populate your database.</li>
	<li>A <a href="documents/README.md">README.md</a> file containing:
		<ul>
			<li>Dependencies (external libraries)</li>
			<li>How to setup the framework.</li>
			<li>How to populate and setup the database.</li>
			<li>How to setup (e.g. modifying any configuration files) and run your RESTful API.</li>
			<li>The URL to access your API (usually <em>nameofapplication/api/version/</em>)=&gt; the path to your application.</li>
		</ul>
	</li>
</ol>
<em>Do not forget to include in the <a href="doc/README.md">README.md</a> file which is the path to access to your application remotely.</em>

<strong>NOTE: Your code MUST be clearly documented. </strong>For each public method/function you must provide: a short description of the method, input parameters, output parameters, exceptions (when the application can fail and how to handle such fail). 
&nbsp;<strong>In addition should be clear which is the code you have implemented yourself and which is the code that you have borrowed from other sources. Always provide a link to the original source. This includes links to the course material.</strong>
</bloquote>

</details>

---
:pencil2: *You do not need to write anything in this section, just complete the implementation.*

---

### RESTful API testing
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
:pencil2: *Most important part of this section is completing the implementation. Write down here a short reflection on which are the main errors you have solved thanks to the functional tests.*

---

## REST conformance

<details>
<summary>
:bookmark_tabs:&nbsp;&nbsp;<strong>Content that must be included in the section</strong>
</summary>

<bloquote>
Explain briefly how your API meets REST principles. Focus specially in these three principles: <strong>Addressability, Uniform interface, Statelessness</strong>. Provide examples (e.g. how does each HTTP method work in your API). Note that Connectedness will be addressed in more depth in Deadline 4.
</bloquote>

</details>

---

:pencil2: *Write your text here*

---

## Extras

<details>
<summary>
:bookmark_tabs:&nbsp;&nbsp;<strong>Details on extra features</strong>
</summary>
<bloquote>
This section lists the additional features that will be graded as part of the API but are not required. In addition to implementing the feature you are also asked to write a short description for each.
</bloquote>

</details>

### URL Converters

<details>
<summary>
:bookmark_tabs:&nbsp;&nbsp;<strong>Fill this section if you used URL converters</strong>
</summary>
<bloquote>
Write a short rationale of how URL converters are used, including your thoughts on the possible trade-offs. Go through all URL parameters in your API and describe whether they use a converter, what property is used for converting, or why it's not using a converter.
</bloquote>
</details>

---

:pencil2: *Write your text here*

---

### Schema Validation

<details>
<summary>
:bookmark_tabs:&nbsp;&nbsp;<strong>Fill this section if you used JSON schema validation</strong>
</summary>
<bloquote>
Write a short description of your JSON schemas, including key decision making for choosing how to validate each field. 
</bloquote>
</details>

---

:pencil2: *Write your text here*

---

### Caching

<details>
<summary>
:bookmark_tabs:&nbsp;&nbsp;<strong>Fill this section if you implemented server side caching</strong>
</summary>
<bloquote>
Explain your caching decisions here. Include an explanation for every GET method in your API, explaining what is cached (or why it is not cached), and how long is it cached (and why). If you are using manual cache clearing, also explain when it happens.
</bloquote>
</details>

---

:pencil2: *Write your text here*

---

### Authentication

<details>
<summary>
:bookmark_tabs:&nbsp;&nbsp;<strong>Fill this section if you implemented authentication</strong>
</summary>
<bloquote>
Explain your authentication scheme here. Describe the authentication requirements for each resource in your API, and your reasoning for the decisions. In addition, provide a plan for how API keys will be distributed, even if the distribution is not currently implemented.
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


