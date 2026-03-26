from crew.crew import run_pipeline

def main():
    final_content, final_review = run_pipeline()

    print("\n" + "="*60)
    print("FINAL APPROVED CONTENT:")
    print("="*60)
    print(final_content)

    print("\n" + "="*60)
    print("FINAL EDITOR REVIEW:")
    print("="*60)
    print(final_review)

if __name__ == "__main__":
    main()
