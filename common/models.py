from pydantic import BaseModel, Field


class PackageQuery(BaseModel):
    name: str = Field(min_length=1, max_length=100, pattern=r"^[A-Za-z0-9.+_-]+$")
    version: str | None = Field(default=None, max_length=50)


class ReportRequest(BaseModel):
    source_file: str = Field(min_length=1, max_length=200)
    output_file: str = Field(default="report.md", min_length=1, max_length=200)
