package hello

import (
 "net/http"
 "context"
 "fmt"
 "log"

 "cloud.google.com/go/datastore"
)

func Hi(w http.ResponseWriter, r *http.Request) {
 fmt.Fprintf(w, "Hello, World!")
}
