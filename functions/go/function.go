package hello

import (
 "net/http"
 "context"
 "fmt"
 "os"
 "log"

 "cloud.google.com/go/datastore"
)

type CaseStudy struct {
	OrganisationName string
	Address string
	PointOfContact string
	PositionInOrganisation string
	Email string
	Phone string
	StartDate string
	CompletionDate string
	EstimatedValue string
	ClientRefContactFirst string
}

func Hi(w http.ResponseWriter, r *http.Request) {
	ctx := context.Background()
	projectID := os.Getenv("PROJECT_ID")

	client, err := datastore.NewClient(ctx, projectID)
	if err != nil {
		log.Fatalf("Failed to create client: %v", err)
	}

	// Sets the kind for the new entity.
	kind := "CaseStudy"
	// Sets the name/ID for the new entity.
	name := "samplecasestudy1"
	// Creates a Key instance.
	taskKey := datastore.IncompleteKey(kind, nil)

	// Creates a Task instance.
	caseStudy := CaseStudy{
		OrganisationName: "ACME Widget Factory",
	}

	// Saves the new entity.
	if _, err := client.Put(ctx, taskKey, &caseStudy); err != nil {
		log.Fatalf("Failed to save case study: %v", err)
	}

	fmt.Printf("Saved %v: %v\n", taskKey, caseStudy.OrganisationName)
	fmt.Fprintf(w, "Saved %v: %v\n", taskKey, caseStudy.OrganisationName)
}
