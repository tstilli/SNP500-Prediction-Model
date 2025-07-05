import os
import json
from database import get_db_session, SECFilings 
#from tqdm import tqdm  

DATA_DIR = "S:\\Repositories\\vectorDB\\data\\silver"

def load_all_filings():
    session = get_db_session()
    json_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.json')]
    
    for file_name in tqdm(json_files, desc="Loading filings"):
        file_path = os.path.join(DATA_DIR, file_name)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                chunks = json.load(f)

            records = []
            for chunk in chunks:
                record = SECFilings(
                    accession_number=chunk.get("accession_number"),
                    chunk_id=chunk.get("chunk_id"),
                    text=chunk.get("text"),
                    company_name=chunk.get("company_name"),
                    filing_date=chunk.get("filing_date"),
                    form_type=chunk.get("form_type"),
                    cik=chunk.get("cik"),
                    source_file=chunk.get("source_file"),
                    metadata_json={} 
                )
                records.append(record)

            session.bulk_save_objects(records)

        except Exception as e:
            print(f"Error loading {file_name}: {e}")
    
    session.commit()
    session.close()
    print("Finished loading all filings.")

if __name__ == "__main__":
    load_all_filings()