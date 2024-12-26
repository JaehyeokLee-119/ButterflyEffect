## Installation

1. **Create and Activate Environment**
   ```sh
   # Create a new conda environment
   conda create -n butterfly python=3.9.17

   # Activate the environment
   conda activate butterfly
   ```
   
2. **Install Required Libraries**
   ```sh
   # Install Required Libraries
   pip install -r requirements.txt
   ```

4. **Download and Unzip Wiki Data**
   ```sh
   # Download wiki data
   wget https://nlp.stanford.edu/projects/hotpotqa/enwiki-20171001-pages-meta-current-withlinks-abstracts.tar.bz2

   # unzip wiki data
   tar -jxvf enwiki-20171001-pages-meta-current-withlinks-abstracts.tar.bz2
   ```

5. **Set OpenAI API Key**
   ```sh
   #Set OpenAI API Key as Environment Variable
   export OPENAI_API_KEY='your_api_key_here'
   ```
## Preprocess

* **Preprocess and Embedding Wiki**
   ```sh
   #Preprocess Wiki Data
   python preprocess_wiki.py

   #Embedding Wiki Data
   python embedding_wiki.py
   ```
## Inference

* **Inference**
   ```sh
   # Run Inference
   sh infer.sh
   ```
   
