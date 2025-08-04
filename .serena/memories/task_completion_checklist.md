# Task Completion Checklist

## After Making Code Changes

### Testing
1. **Run Full Test Suite**: `pytest tests/` - Ensure all tests pass
2. **Run Specific Tests**: For modified modules, run specific test files
3. **Manual API Testing**: Test modified endpoints via `/api/v1/docs` or curl

### Code Quality
- **No Linting Tool**: Project doesn't use flake8/black/pylint - follow existing style
- **Documentation**: Update docstrings if function signatures change
- **Error Handling**: Ensure proper HTTPException usage for API errors

### Functionality Verification
1. **Server Startup**: Verify `uvicorn elite_status.main:app --reload` works
2. **API Documentation**: Check `/api/v1/docs` loads correctly
3. **File Monitoring**: Ensure watchdog functionality works if modified
4. **Environment Variables**: Test ELITE_STATUS_PATH detection if changed

### Integration Testing
- **Cross-platform**: Consider Windows/Linux compatibility
- **Network Access**: Verify CORS and network accessibility
- **Authentication**: Test token-based auth if implemented

### Environment Considerations
- **Conda Environment**: Test with `conda activate elite` if available
- **Dependencies**: Check requirements.txt if new imports added
- **File Permissions**: Verify uinput permissions on Linux

## Before Committing
1. Run `pytest tests/` to ensure all tests pass
2. Check that the server starts without errors
3. Verify API documentation is accessible
4. Test critical endpoints manually if significant changes made

## Special Considerations
- **Elite Dangerous Integration**: Test with actual game files if available
- **Network Security**: Review CORS settings for production
- **System Dependencies**: Verify python-uinput requirements on target systems