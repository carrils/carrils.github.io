---
layout: archive
title: "Playing With FHIR"
permalink: /playing-with-fhir/
excerpt: "Annotated examples of how to use the HAPI FHIR Java framework"
collection: portfolio
#author_profile: true
---

[This](https://github.com/carrils/playing-with-fhir) is a github repo that hosts the codebase I created to study/support
FHIR knowledge transfers and office hours while supporting the Public Health FHIR Implementation Collaborative (PHFIC)
project.
The examples served as templates for STLT Health departments to use as a starting point and study resource for their own
implementations.

They are created with the HAPI FHIR framework.
HAPI FHIR is a complete implementation of the [HL7 FHIR](http://hl7.org/fhir/) standard for healthcare interoperability
in Java.

# Examples

### Creating a FHIR patient

```java
Patient pat = new Patient();
HumanName name = pat.addName().setFamily("Aquato").addGiven("Razputin").addGiven("E");

// NOTE: You will need to update the identifier value if you want to uploade a new patient as you cannot upload duplicates
Identifier identifier = pat.addIdentifier().setSystem("MEDSS").setValue("45D783B411");
ContactPoint telecom = pat.addTelecom().setSystem(ContactPointSystem.PHONE).setUse(ContactPointUse.HOME).setValue("488 715-9846");
pat.setGender(Enumerations.AdministrativeGender.MALE).setBirthDate(new Date(92, 8, 12));
Address address = pat.addAddress().setUse(Address.AddressUse.HOME).addLine("101 main str").setCity("Minneapolis").setState("MN").setPostalCode("55403");
Communication communication = (Communication) new Communication().setLanguage("en");

```

### Customizing the patient with extensions
Using the previously created patient:
```java

// Add Race to fhir patient via an extension (StringType is just a FHIR String data type)
pat.addExtension("http://hl7.org/fhir/us/core/StructureDefinition/us-core-race", new StringType("Asian"));

// Add Ethnicity via extension
pat.addExtension("http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity", new StringType("Not Hispanic or Latino"));

// Add Gender Identity via extension
pat.addExtension("http://hl7.org/fhir/us/core/STU5.0.1/StructureDefinition-us-core-genderIdentity.html", new StringType("M"));

// Add Birthsex via Extension
pat.addExtension("http://hl7.org/fhir/us/core/STU5.0.1/StructureDefinition-us-core-birthsex.html", new StringType("M"));
```

### Encoding a FHIR patient to JSON or XML

```java
// Encode fhir patient to JSON
IParser jsonParser = contextR4.newJsonParser().setPrettyPrint(true);
jsonEncoded = jsonParser.encodeResourceToString(pat);

// Encode fhir patient to XML
IParser xmlParser = contextR4.newXmlParser().setPrettyPrint(true);
xmlEncoded = xmlParser.encodeResourceToString(patient);
```

### Creating a Generic (Fluent) Client

```java
// the server base url for your server
String serverBase = "http://hapi.fhir.org/baseR4";

// create a context and then a client factory object from it
FhirContext contextR4 = FhirContext.forR4();
IRestfulClientFactory clientFactory = contextR4.getRestfulClientFactory();

// can configure the client factory, here i just increase the timeout value & turn off server validation
clientFactory.setServerValidationMode(ServerValidationModeEnum.NEVER);
clientFactory.setConnectTimeout(60 * 1000);
clientFactory.setSocketTimeout(60 * 1000);
// create a capturing interceptor
CapturingInterceptor capturer = new CapturingInterceptor();

// create a generic client
IGenericClient client = contextR4.newRestfulGenericClient(serverBase);
// register the capturing interceptor for the generic client
client.registerInterceptor(capturer);
```
### uploading a FHIR patient resource to a FHIR server with that client

```java
try {
    // Send resource up to the server - the result of the send operation is stored in outcome
    MethodOutcome outcome = client.create()
            .resource(pat)
            .prettyPrint()
            .encodedJson()
            .execute();
    // Retrieve id from outcome
    IdType id = (IdType) outcome.getId();
    System.out.println("Resource is available at: " + id.getValue());

    // System.out.println("[OUTCOME]\n" + outcome.toString());

    // Retrieve patient from outcome
    Patient receivedPatient = (Patient) outcome.getResource();
    System.out.println("This is what we sent up: \n" + jsonParser.encodeResourceToString(pat) + "\n");
    System.out.println("And this is what we received back: \n" + jsonParser.encodeResourceToString(receivedPatient));
} catch (DataFormatException e) {
    System.out.println("An error occurred trying to upload:");
    e.printStackTrace();
}
```

### Searching a given FHIR server with that client

```java
// Create a 'search' bundle to search a FHIR server for a patient & execute it with the client
//  We use a pre-uploaded example patient with identifier values:
//  "system": "http://www.health.state.mn.us/diseases/reportable/medss/",
//  "value": "45D783B1"
Bundle searchPatExample = client.search().forResource(Patient.class)
        .where(Patient.IDENTIFIER.exactly().systemAndCode("http://www.health.state.mn.us/diseases/reportable/medss/", "45D783B1"))
        .returnBundle(Bundle.class)
        .execute();
        // write search results to json file
        try {
            Writer outf = new FileWriter("searched-patient-example.json");
            outf.write(jsonParser.encodeResourceToString(searchPatExample));
            outf.close();
        } catch (Exception e) {
            System.out.println("Well, now look what you've done.\n");
            e.getStackTrace();
        }
        // print result
        System.out.println("The resource returned from searching the FHIR server:\n" + jsonParser.encodeResourceToString(searchPatExample));
```

### Validating a FHIR resource with a validator

```java
// Ask the context for a validator
FhirValidator validator = contextR4.newValidator();

// Create a validation support module and register it with the validator
DefaultProfileValidationSupport structures = new DefaultProfileValidationSupport(contextR4); // this object supplies the structure definitions
IValidatorModule module = new FhirInstanceValidator(structures);
validator.registerValidatorModule(module);

// Pass patient resource to validator
ValidationResult result = validator.validateWithResult(jsonParser.encodeResourceToString(pat));
// The result object now contains the validation results
for (SingleValidationMessage next : result.getMessages()) {
    System.out.println(next.getLocationString() + " " + next.getMessage());
}
```
