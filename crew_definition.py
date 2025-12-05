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
                'in a user-friendly format with all necessary information including proper attribution, '
                'download links, and usage guidelines. You understand that URLs must be preserved '
                'EXACTLY as provided - you never create, modify, or shorten URLs. You copy-paste '
                'URLs verbatim to ensure they work correctly for users.'
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
                        'For each query, request 10-15 photos. Review all results and select the TOP 8-12 '
                        'photos that best match the user\'s original request: "{prompt}". '
                        'Consider photo quality, relevance, composition, and variety in your selection. '
                        '\n\nIMPORTANT: You must copy the EXACT URLs from the Pexels API response. '
                        'Do NOT modify or create new URLs. Use the exact Original, Large, Medium, and Small '
                        'URLs provided by the API for each selected photo.'
                    ),
                    expected_output=(
                        'A curated collection of 8-12 high-quality stock photos. For EACH photo include: '
                        'Photo ID, the EXACT Original URL, EXACT Large URL, EXACT Medium URL, EXACT Small URL, '
                        'photographer name, photographer profile URL, dimensions, Pexels page URL. '
                        'Copy these URLs EXACTLY as provided by the Pexels API - do not modify them.'
                    ),
                    agent=photo_curator
                ),
                Task(
                    description=(
                        'Take the curated photo selection and format it into a clear, well-organized presentation. '
                        'For each photo include: Photo ID, all size URLs (original, large, medium, small), '
                        'photographer name and profile link, dimensions, and Pexels page URL. '
                        '\n\nCRITICAL: Use the EXACT URLs provided by the curator. Copy and paste them EXACTLY '
                        'as they are - do NOT modify, shorten, or create new URLs. These must be working links. '
                        '\n\nInclude a note about attribution requirements: "Photos provided by Pexels. '
                        'Please provide attribution by linking to the photographer\'s Pexels profile."'
                    ),
                    expected_output=(
                        'A professionally formatted list of selected stock photos with complete download information. '
                        'Each photo must include: number, title/description, Photo ID, EXACT clickable URLs '
                        '(Original, Large, Medium, Small) copied verbatim from the curator, photographer name '
                        'with profile link, dimensions, Pexels page URL, and attribution note. '
                        'All URLs must be the EXACT ones provided - working, clickable links.'
                    ),
                    agent=results_formatter
                )
            ]
        )
        self.logger.info("Crew setup completed")
        return crew