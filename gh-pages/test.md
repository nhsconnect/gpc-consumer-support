---
title: Introduction to GP Connect API
keywords: homepage
permalink: index.html
toc: false
summary: A brief introduction to getting started with the GP Connect FHIR&reg; APIs
---

**Draft**

![Test svg](images/test.svg)

<img src="images/test.svg">

<embed type="image/svg+xml" src="images/test.svg" />

<object type="image/svg+xml" data="images/test.svg">
    <!-- Your fall back here -->
    <img src="images/test.svg" />
</object>


## Welcome to the GP Connect Consumer Support Hub

This site is designed to help consumer organisations interested in developing GP Connect products understand the requirements and processes involved.
You may be a consumer organisation working with an end-user organisation that wants to use GP Connect to support direct patient care or you may be looking to develop GP Connect APIs to secure a place in the healthcare market.

GP Connect has worked with the GP clinical system suppliers to develop the APIs. These APIs make data from GP clinical systems available in a standard form so that the data can be used across different systems.

We've provided some information below about the GP Connect products that are currently available for consumer organisations to develop. Note that GP Connect products can only be used for _direct patient care_ of NHS patients.

More detailed information can be found on our [website.](https://digital.nhs.uk/services/gp-connect)

### Access Record
Access Record products allow authorised clinicians to access GP patient records. Access Record has two methods of retrieving data from the patient record:  

* Access Record: HTML enables a read-only view of a patient’s record regardless of the practice clinical system. The record can be viewed within another care setting including (but not exclusive to) another GP practice, an urgent care call centre, or an acute care organisation via an accredited system or application.

* Access Record: Structured provides access to a patient’s record in a machine-readable, structured, and coded format.  Structured data allows the consuming system to import and process patient data provided that its only used for direct care, and where the system meets the specified GP Connect consumer requirements, including information governance and clinical safety standards.

### Send Document        
Send Document provides a simple and standardised way of updating a patient record. It sends a consultation summary in PDF format that may have taken place away from the patient's registered practice. Each message sent using Send Document makes use of the GP Connect Messaging components ITK3 and MESH to deliver the message. 

### Appointment Management   
GP Connect: Appointment Management is used to book appointments on behalf of a patient into their registered practice or another care setting. This is useful for services such as NHS 111 and Primary Care Networks.


If you are interested in developing any of our GP Connect products please see the links below to the technical specifications and read the information held on our [GP Connect prerequisites and expressing an interest](https://github.com/nhsconnect/gpc-consumer-support/wiki/GP-Connect-Prerequisites-and-expressing-an-interest) page.

### GP Connect technical specifications
Our specification homepage can be found here: [GP Connect specifications for developers - NHS Digital](https://digital.nhs.uk/services/gp-connect/gp-connect-specifications-for-developers)

For product-specific pages:

* [Access Record HTML](https://developer.nhs.uk/apis/gpconnect-0-7-3/accessrecord.html)

* [Access Record Structured](https://developer.nhs.uk/apis/gpconnect-1-2-7/accessrecord_structured.html)

* [Send Document](https://developer.nhs.uk/apis/gpconnect-messaging-1-3/senddocument.html)

* [Appointment Management](https://developer.nhs.uk/apis/gpconnect-1-2-7/appointments.html)

**Note:** You are advised not to develop against specifications that are marked as beta until they are baselined and published. If you choose to develop ahead of this, you do so at your own risk. 
