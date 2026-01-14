/**
 * Base API client with fetch wrapper and error handling
 */

const API_BASE = 'http://localhost:8000';

/**
 * Custom error class for API errors
 */
export class ApiError extends Error {
	constructor(
		public status: number,
		message: string,
	) {
		super(message);
		this.name = 'ApiError';
	}
}

interface RequestOptions extends RequestInit {
	params?: Record<string, string>;
}

/**
 * Generic fetch wrapper with error handling
 */
export async function request<T>(
	endpoint: string,
	options: RequestOptions = {},
): Promise<T> {
	const { params, ...fetchOptions } = options;

	let url = `${API_BASE}${endpoint}`;
	if (params) {
		const searchParams = new URLSearchParams(params);
		url += `?${searchParams}`;
	}

	const response = await fetch(url, {
		...fetchOptions,
		headers: {
			'Content-Type': 'application/json',
			...fetchOptions.headers,
		},
	});

	if (!response.ok) {
		const error = await response
			.json()
			.catch(() => ({ detail: 'Unknown error' }));
		throw new ApiError(response.status, error.detail ?? 'Request failed');
	}

	// Handle 204 No Content
	if (response.status === 204) {
		return undefined as T;
	}

	return response.json();
}
