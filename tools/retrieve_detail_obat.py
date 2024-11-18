from pydantic.v1 import BaseModel, Field, validator
from typing import Optional, List
from langchain_core.tools import StructuredTool, ToolException, tool
from config.configs import OPENAI_API_KEY, GROQ_API_KEY, NEO4J_CONNECTION_URL, NEO4J_USER, NEO4J_API_KEY
from langchain_community.graphs import Neo4jGraph

graph = Neo4jGraph(NEO4J_CONNECTION_URL, NEO4J_USER, NEO4J_API_KEY)

class Input(BaseModel):
    nama_obat: Optional[List[str]] = Field(description="Nama obat. Harus dalam list. Pastikan hanya nama obatnya saja")
    komposisi_obat: Optional[List[str]] = Field(description="Nama komposisi obat. Harus dalam list")
    penyakit: Optional[List[str]] = Field(description="Nama penyakit. Harus dalam list")

def retrieve_detail_obat(
    nama_obat: Optional[List[str]] = [],
    komposisi_obat: Optional[List[str]] = [],
    penyakit: Optional[List[str]] = []
) -> str:
    """Useful for when you need to retrieve all drugs data from db"""

    # print(nama_obat, komposisi_obat, penyakit)

    params = {}
    filters = []

    base_query = """
    MATCH (o:Obat)-[:MENGANDUNG]->(k:Komposisi)
    MATCH (o)-[:MENGOBATI]->(p:Penyakit)
    """

    if nama_obat:
      # candidate_drugs = [el["candidate"] for el in get_candidates(obat, "obat")]
      # if not candidate_drugs:
      #   return "The mentioned drug was not found"
      nama_obat = [item.lower() for item in nama_obat]
      filters.append("o.nama IN $nama_obat")
      params["nama_obat"] = nama_obat

    if komposisi_obat:
      # candidate_drugs = [el["candidate"] for el in get_candidates(obat, "obat")]
      # if not candidate_drugs:
      #   return "The mentioned drug was not found"
      komposisi_obat = [item.lower() for item in komposisi_obat]
      filters.append("k.nama IN $komposisi_obat")
      params["komposisi_obat"] = komposisi_obat

    if penyakit:
      # candidate_drugs = [el["candidate"] for el in get_candidates(obat, "obat")]
      # if not candidate_drugs:
      #   return "The mentioned drug was not found"
      penyakit = [item.lower() for item in penyakit]
      filters.append("p.nama IN $penyakit")
      params["penyakit"] = penyakit

    if filters:
      base_query += " WHERE "
      base_query += " AND ".join(filters)
      base_query += """
      WITH o, collect(DISTINCT k.nama) AS komposisi, collect(DISTINCT p.nama) AS penyakit
      RETURN o.nama AS Obat, komposisi AS Komposisi, penyakit AS Penyakit
      """
      # print(f"Using parameters: {params}")
      # print(base_query)
      data = graph.query(base_query, params=params)

    return data

retrieve_detail_obat_tool = StructuredTool.from_function(
    func=retrieve_detail_obat,
    args_schema= Input,
    handle_tool_error=True,
)


