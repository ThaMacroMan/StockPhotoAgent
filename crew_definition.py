import os
from crewai import Agent, Crew, Task, LLM
from logging_config import get_logger
from pexels_tool import PexelsSearchTool


class PhotoSearchCrew:
    def __init__(self, verbose=True, logger=None, model=None):
        self.verbose = verbose
        self.logger = logger or get_logger(__name__)
        
        # Check OpenAI API key
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            self.logger.info(f"OpenAI API key found: {openai_key[:10]}...{openai_key[-4:] if len(openai_key) > 14 else '***'}")
        else:
            self.logger.warning("OPENAI_API_KEY not found in environment variables!")
        
        # Configure LLM - support custom model, default to gpt-5-mini
        try:
            if model:
                self.logger.info(f"Initializing LLM with custom model: {model}")
                self.llm = LLM(model=model)
                self.logger.info(f"LLM initialized successfully with model: {model}")
            else:
                default_model = "gpt-5-mini"
                self.logger.info(f"Initializing LLM with default model: {default_model}")
                self.llm = LLM(model=default_model)
                self.logger.info(f"LLM initialized successfully with default model: {default_model}")
        except Exception as e:
            self.logger.error(f"Failed to initialize LLM: {str(e)}", exc_info=True)
            raise
        
        # Initialize Pexels tool
        pexels_api_key = os.getenv("PEXELS_API_KEY")
        if not pexels_api_key:
            raise ValueError("PEXELS_API_KEY not found in environment variables")
        
        self.pexels_tool = PexelsSearchTool(api_key=pexels_api_key)
        self.crew = self.create_crew()
        self.logger.info("PhotoSearchCrew initialized")

    def create_crew(self):
        self.logger.info("Creating photo search crew with agents")
        
        # Agent 1: Query Analyst - Understands user intent and refines search terms
        query_analyst = Agent(
            role='Search Query Specialist',
            goal='Analyze user prompts and extract the most effective search terms for finding relevant stock photos',
            backstory=(
                'You are an expert at understanding creative briefs and translating them into precise search queries. '
                'You know how to break down complex requests into specific, searchable keywords that will yield '
                'the best stock photo results. You consider mood, style, subject matter, and context.'
            ),
            llm=self.llm,
            verbose=self.verbose
        )

        # Agent 2: Photo Curator - Searches and selects the best photos
        photo_curator = Agent(
            role='Stock Photo Curator',
            goal='Search Pexels for high-quality stock photos that perfectly match the user\'s needs',
            backstory=(
                'You are a professional photo curator with an eye for quality and relevance. '
                'You use the Pexels API to find photos and select the most appropriate ones based on '
                'composition, quality, relevance, and usability for various projects. '
                'You are meticulous about preserving exact URLs from the API responses - you NEVER '
                'modify, shorten, or recreate URLs. You copy them exactly as provided.'
            ),
            tools=[self.pexels_tool],
            llm=self.llm,
            verbose=self.verbose
        )

        # Agent 3: Results Formatter - Organizes and presents the final selection
        results_formatter = Agent(
            role='Results Presenter',
            goal='Format and present the selected photos in a clear, organized, and actionable way',
            backstory=(
                'You are a presentation specialist who knows how to organize photo results '
                'in a user-friendly markdown format with all necessary information including proper attribution, '
                'download links, and usage guidelines. You understand that markdown links must be preserved '
                'EXACTLY as provided in the format [Link Text](URL). You never create, modify, or shorten '
                'markdown links. You copy-paste them verbatim to ensure they work correctly for users.'
            ),
            llm=self.llm,
            verbose=self.verbose
        )

        self.logger.info("Created query analyst, photo curator, and results formatter agents")

        crew = Crew(
            agents=[query_analyst, photo_curator, results_formatter],
            tasks=[
                Task(
                    description=(
                        'Analyze this user request: "{prompt}"\n\n'
                        'Extract 2-4 effective search queries that will find the most relevant stock photos. '
                        'Consider synonyms, related concepts, and different ways to describe what the user needs. '
                        'Be specific and creative with your search terms.'
                    ),
                    expected_output=(
                        'A list of 2-4 optimized search queries with brief explanations of why each query '
                        'will help find relevant photos for the user\'s request.'
                    ),
                    agent=query_analyst
                ),
                Task(
                    description=(
                        'Using the search queries from the analyst, search Pexels for stock photos. '
                        'For each query, request 15-18 photos to ensure a wide selection while keeping data manageable. '
                        'Review all results and select 5 photos total, organized into TWO categories for the user\'s request: "{prompt}": '
                        '\n\nCATEGORY 1 - Closest Matches (2-3 photos): '
                        'Select 2-3 photos that are the MOST DIRECT match to the user\'s original request. '
                        'These should match the prompt as closely as possible in subject, style, mood, and context. '
                        '\n\nCATEGORY 2 - Varied but Related (2-3 photos): '
                        'Select 2-3 photos that are still related to the prompt but offer more variety - different angles, '
                        'compositions, styles, or interpretations while still being relevant. These should complement the '
                        'closest matches by providing alternative perspectives. '
                        '\n\nUse the photo descriptions (alt text) to understand what each photo contains. For EACH photo include: '
                        'Photo description, Photo ID, photographer name with markdown link, dimensions, Pexels page link, '
                        'Thumbnail URL, and Original download link. Clearly label which category each photo belongs to. '
                        '\n\nIMPORTANT: You must copy the EXACT URLs from the Pexels API response. '
                        'Do NOT modify or create new URLs. Use the exact Pexels page URL and Original photo URL '
                        'provided by the API for each selected photo.'
                    ),
                    expected_output=(
                        'A curated collection of 5 photos organized into two categories. For EACH photo include: '
                        'Category label (Closest Match OR Varied/Related), Photo description, Photo ID, photographer name with markdown link, '
                        'dimensions, Pexels page link, Thumbnail URL, and Original download link, all formatted as markdown links. '
                        'Preserve the EXACT markdown link format from the search results - do not modify the URLs.'
                    ),
                    agent=photo_curator
                ),
                Task(
                    description=(
                        'Take the curated selection of 5 photos (organized into two categories by the curator) and format them into TWO SECTIONS. '
                        '\n\nSECTION 1 - Closest Matches: '
                        'Create a section header "## Closest Matches" and list the 2-3 photos labeled as "Closest Match" by the curator. '
                        '\n\nSECTION 2 - More Varied Options: '
                        'Create a section header "## More Varied Options" and list the 2-3 photos labeled as "Varied/Related" by the curator. '
                        '\n\nFor each photo in both sections, display a SINGLE thumbnail image (HTML format only) with all details inline on the same line. '
                        'Format: <img src="thumbnail_url" alt="Photo description" width="200" style="vertical-align:middle; margin-right:10px;" /> '
                        '**Description** | Photographer: [Name](url) | Dimensions: WxH | [Pexels](url) | [Original](url) '
                        '\n\nCRITICAL FORMATTING RULES: '
                        '1) Organize photos into TWO distinct sections with clear headers '
                        '2) Use ONLY HTML img tag (no markdown images) with width="200" for compact thumbnails '
                        '3) Place image and details on the SAME LINE (inline layout) '
                        '4) DO NOT include Photo ID - exclude it completely '
                        '5) Use vertical-align:middle on the image so text aligns nicely '
                        '6) Preserve the EXACT URLs from the curator - do NOT modify, shorten, or recreate them '
                        '\n\nInclude a note about attribution requirements: "Photos provided by Pexels. '
                        'Please provide attribution by linking to the photographer\'s Pexels profile."'
                    ),
                    expected_output=(
                        'A formatted output with TWO SECTIONS: '
                        '\n\n## Closest Matches '
                        'List of 2-3 photos (labeled as Closest Match by curator), each on a single line: '
                        '<img src="thumbnail_url" alt="description" width="200" style="vertical-align:middle; margin-right:10px;" /> '
                        '**Description** | Photographer: [Name](url) | Dimensions: WxH | [Pexels](url) | [Original](url) '
                        '\n\n## More Varied Options '
                        'List of 2-3 photos (labeled as Varied/Related by curator), each on a single line with same format. '
                        'NO Photo ID should be included. Use the Thumbnail URL from the search results. Copy all URLs EXACTLY from the curator. '
                        'Include attribution note at the end.'
                    ),
                    agent=results_formatter
                )
            ]
        )
        self.logger.info("Crew setup completed")
        return crew