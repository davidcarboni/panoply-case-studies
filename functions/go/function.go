package hello

import (
 "fmt"
 "net/http"
)

func Hi(w http.ResponseWriter, r *http.Request) {
 fmt.Fprintf(w, "Hello, World!")
}
