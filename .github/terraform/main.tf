provider "google" {
  credentials = var.gcp_credentials
  project     = var.gcp_project_id
  region      = "us-central1"
}

variable "gcp_credentials" {
  description = "Google Cloud Platform credentials as JSON"
}

variable "gcp_project_id" {
  description = "Google Cloud Project ID"
}

variable "db_password" {
  description = "Database Password"
}

resource "google_sql_database_instance" "example" {
  name             = "example-instance"
  database_version = "POSTGRES_13"
  region           = "us-central1"
  settings {
    tier = "db-f1-micro"
  }
}

resource "google_sql_database" "example_db" {
  name     = "example-db"
  instance = google_sql_database_instance.example.name
  charset  = "UTF8"
  collation = "en_US.UTF8"
}

resource "google_sql_user" "example_user" {
  name     = "example-user"
  instance = google_sql_database_instance.example.name
  password = var.db_password
}

output "connection_name" {
  value = google_sql_database_instance.example.connection_name
}
