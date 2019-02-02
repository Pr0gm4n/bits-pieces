#! /usr/bin/Rscript --vanilla
# taken from http://rmarkdown.rstudio.com/articles_beamer.html
library(knitr)
library(rmarkdown)
file <- list.files(pattern='.Rmd')
rmarkdown::render(file)
if (file == "presentation.Rmd") {
  rmarkdown::render(file, output_format = "pdf_document", output_file = "notes.pdf")
}
