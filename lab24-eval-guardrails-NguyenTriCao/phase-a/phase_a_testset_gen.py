import os
import asyncio
from dotenv import load_dotenv
from ragas.testset import TestsetGenerator
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.testset.synthesizers import (
    SingleHopSpecificQuerySynthesizer,
    MultiHopAbstractQuerySynthesizer,
    MultiHopSpecificQuerySynthesizer
)
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Load environment variables
load_dotenv()

def generate_testset():
    print("Loading documents...")
    # Loading .md files from data folder
    loader = DirectoryLoader("data", glob="**/*.md", loader_cls=TextLoader, loader_kwargs={'encoding': 'utf-8'})
    documents = loader.load()
    print(f"Loaded {len(documents)} documents.")

    print("Initializing TestsetGenerator...")
    # Wrap LangChain models for Ragas 0.4.x
    generator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o-mini"))
    generator_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings())

    # Initialize the generator
    generator = TestsetGenerator(
        llm=generator_llm,
        embedding_model=generator_embeddings
    )

    print("Initializing Synthesizers...")
    # In 0.4.x, we instantiate the synthesizers
    # and pass them to query_distribution as a list of (instance, weight)
    # Simple -> SingleHopSpecific
    # Reasoning -> MultiHopSpecific
    # Multi-context -> MultiHopAbstract
    
    # We need to initialize the synthesizers with the LLM
    single_hop = SingleHopSpecificQuerySynthesizer(llm=generator_llm)
    multi_hop_specific = MultiHopSpecificQuerySynthesizer(llm=generator_llm)
    multi_hop_abstract = MultiHopAbstractQuerySynthesizer(llm=generator_llm)

    query_distribution = [
        (single_hop, 0.5),
        (multi_hop_specific, 0.25),
        (multi_hop_abstract, 0.25)
    ]

    print("Generating test set (size=50)...")
    from ragas.run_config import RunConfig
    run_config = RunConfig(max_workers=2, timeout=300)

    testset = generator.generate_with_langchain_docs(
        documents=documents,
        testset_size=5,
        query_distribution=query_distribution,
        with_debugging_logs=True,
        raise_exceptions=False,
        run_config=run_config
    )

    print("Saving test set to csv...")
    df = testset.to_pandas()
    output_path = os.path.join("lab24-eval-guardrails", "phase-a", "testset_v1.csv")
    df.to_csv(output_path, index=False)
    print(f"Test set saved to {output_path}")
    
    # Verify distribution
    if 'synthesizer_name' in df.columns:
        print("\nDistribution of synthesizer types:")
        print(df['synthesizer_name'].value_counts())

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in environment.")
    else:
        generate_testset()
